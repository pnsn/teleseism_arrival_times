#!/usr/bin/env python

'''
Reads the output of get_events.py and calculates the arrival time
of the first P arrival to the approx. closest point in WA & OR.

input in file called 'events_Fetched':
old:
10949281|2018/09/18 12:40:56.960 | 69.5136|-144.1598|  10.8|ak,at,us|NEIC PDE|ak,us2000hgcj,at00pf94kc,ak20257361|ML,5.3,ak|NORTHERN ALASKA

new:
us7000bn4e|2020-09-14T17:54:37.918|44.3103|-115.2201|14.76|us|us|us|us7000bn4e|ml|2.7|us|24 km WNW of Stanley, Idaho
us7000bn3x|2020-09-14T17:15:37.851|44.3537|-115.2153|15.25|us|us|us|us7000bn3x|ml|3.2|us|26 km NW of Stanley, Idaho

output:
2020-07-09 17:15:51   mb,4.4,us  188   118   -2.1   102.0   SOUTHERN SUMATRA, INDONESIA
2020-07-09 16:29:10   mb,4.9,us   10   162  -31.7    58.2   SOUTHWEST INDIAN RIDGE
2020-07-09 16:22:05   mb,4.6,us  245   105   -6.6   128.8   BANDA SEA
2020-07-09 15:54:17  Ml,2.29,MB   13     1   44.4  -115.2   WESTERN IDAHO
'''

from datetime import datetime
from datetime import timedelta
from obspy.geodetics import locations2degrees
import timeit
import math

#----- Function to get good-enough precalculated travel times very quickly.
TT_table_read = False
depths = []
TTs = []
def get_TT(depth,dist):
    global TT_table_read, depths, TTs
    if ( TT_table_read is False ):
        TT_table_read = True
        fTT = open('/home/seis/DAILY_EVENTS/TT.iasp91')
        TTlines = fTT.read().splitlines()
        fTT.close()
        depths = [ -999, 0, 10, 20, 30, 35, 40, 50, 70, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700 ]
        n = 0
        for line in TTlines:
            n = n + 1
            if ( n > 1 ):
                line0 = line.split(' ')
                x = [float(i) for i in line0]
                TTs.append(x)
    iy1 = math.floor(dist)
    iy2 = math.ceil(dist)
    ix = -1
    for d in depths:
        ix = ix + 1
        if ( depth == d ):
            ix1 = ix
            ix2 = ix
        elif ( d > depth ):
            ix2 = ix
            ix1 = ix - 1
            break
    fracX = ( depth - depths[ix1] ) / ( depths[ix2] - depths[ix1] )
    fracY = dist - math.floor(dist)
    TTiy1ix1 = TTs[iy1][ix1]
    TTiy2ix1 = TTs[iy2][ix1]
    TTiy1ix2 = TTs[iy1][ix2]
    TTiy2ix2 = TTs[iy2][ix2]
    TTiyix1 = TTs[iy1][ix1] + fracY * ( TTs[iy2][ix1] - TTs[iy1][ix1] )
    TTiyix2 = TTs[iy1][ix2] + fracY * ( TTs[iy2][ix2] - TTs[iy1][ix2] )
    TT = TTiyix1 + fracX * ( TTiyix2 - TTiyix1 )
    return(TT)

#----- Read the events file

f1 = open("events_Fetched")
lines = f1.readlines()
f1.close()
eventdate = []
eventlat = []
eventlon = []
eventdep = []
eventmag = []
eventloc = []
for i in range(0,len(lines)):
    dt = lines[i].split("|")[1]
    dt2 = datetime.strptime(dt,'%Y-%m-%dT%H:%M:%S.%f')
    eventdate.append(dt2)
    eventlat.append(float(lines[i].split("|")[2]))
    eventlon.append(float(lines[i].split("|")[3]))
    eventdep.append(max(0,float(lines[i].split("|")[4])))
    magnumber = lines[i].split("|")[10]
    magtype = lines[i].split("|")[9]
    magauthor = lines[i].split("|")[11]
    mag = magtype + ',' + magnumber + ',' + magauthor
    eventmag.append(mag)
    eventlocfull = str(lines[i].split("|")[12])
    eventlocmodified = eventlocfull
    if ( 'km ' in eventlocfull and ' of ' in eventlocfull and
         'Oregon' not in eventlocfull and 'Washington' not in eventlocfull ):
        eventlocmodified = eventlocfull.split(' of ')[1]
    eventloc.append(eventlocmodified)

#---- Define a rectangle around WA & OR
latitudes = [ 42.0, 44.33, 46.66, 48.9, 49.0, 49.0, 45.7, 42.0, 42.0, 44.0, 45.9, 47.7, 45.7 ]
longitudes = [ -124.3, -124.0, -124.0, -124.5, -120.8, -117.0, -116.5, -117.0, -120.7, -120.7, -120.5, -120.5, -120.5 ]

for i in range(0,len(lines)):
    #-- check if event is within PNSN boundary
    if ( eventlat[i] >= 41.9 and eventlat[i] <= 49.1 and
         eventlon[i] >= -124.7 and eventlon[i] <= -116.4 ):
        distdeg = 0.
    else:
        distances = []
        for j in range(len(latitudes)):
            distances.append(locations2degrees(eventlat[i],eventlon[i],latitudes[j],longitudes[j]))
        distdeg = min(distances)
    mintime = get_TT( eventdep[i], distdeg )
    T2 = (eventdate[i] + timedelta(seconds = mintime)).replace(microsecond=0)
    Dep = '%3i' % (int(eventdep[i]))
    Mag = '%11s' % (eventmag[i]) 
    DistDeg = '%3i' % (int(distdeg))
    Lat = '%5.1f' % (eventlat[i])
    Lon = '%6.1f' % (eventlon[i])
    print ( str(T2) + "  " + Mag + "  " + Dep + "   " + DistDeg + "  " + Lat + "  " + Lon + "   " + eventloc[i]  )

