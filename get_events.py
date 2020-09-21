#!/usr/bin/env python

'''
Script to poll comcat for events looking back X days from current UTC day
 (hour=0 and minute=0).  X is input argument.

./get_events.py -d 0   (will get all events from UTC today)
./get_events.py -d 7   (will get the past week's events)

Three queries are made and concatinated:
-All global events M >= 4.0
-All events M>= 3.0 within 15 deg radius of 45.82N, 120.8W (center of PNSN)
-All events M>= 2.0 in a box: 41-50 N, 114 to 127W.

Example query using the NEIC API:
https://prod-earthquake.cr.usgs.gov/fdsnws/event/1/query?format=xml&starttime=2014-01-01&endtime=2014-01-02&minmagnitude=5&format=text

output of NEIC API:
#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName
usc000lvb5|2014-01-01T16:03:29.000|-13.8633|167.249|187|us|us|us|usc000lvb5|mww|6.5|us|32km W of Sola, Vanuatu
usc000lv5e|2014-01-01T00:01:16.610|19.0868|120.2389|10.07|us|us|us|usc000lv5e|mb|5.1|us|76km NNW of Davila, Philippines
'''

import argparse
import requests
import sys
import datetime

for i, arg in enumerate(sys.argv):
    if (arg[0] == '-') and arg[1].isdigit(): sys.argv[i] = ' ' + arg
parser = argparse.ArgumentParser()

parser.add_argument('-d','-duration','--d','--duration', action='store', dest='duration',help='duration in days',default=0)
args = parser.parse_args()

now = datetime.datetime.utcnow()
now0 = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
starttime = now0 - datetime.timedelta(days = float(args.duration))
endtime = now + datetime.timedelta(minutes = 1)
starttimestr = starttime.strftime("%Y-%m-%dT%H:%M:%S")
endtimestr = endtime.strftime("%Y-%m-%dT%H:%M:%S")

# Define the middle and boundaries of network
latmiddle = 45.82
lonmiddle = -120.8
latbox1 = 41.
latbox2 = 50.
lonbox1 = -127.
lonbox2 = -114.
maxradiuskm = 15*111.19

# All global events M >= 4.0
url1 = "https://prod-earthquake.cr.usgs.gov/fdsnws/event/1/query?&starttime=" + starttimestr + "&endtime=" + endtimestr + "&minmagnitude=4.0&format=text"
f1 = requests.get(url1)

# All events M>= 3.0 within 15 deg radius of 45.82N, 120.8W (center of PNSN)
url2 = "https://prod-earthquake.cr.usgs.gov/fdsnws/event/1/query?&starttime=" + starttimestr + "&endtime=" + endtimestr + "&latitude=" + str(latmiddle) + "&longitude=" + str(lonmiddle) + "&maxradiuskm=" + str(maxradiuskm) + "&minmagnitude=3.0&format=text"
f2 = requests.get(url2)

# All events M>= 2.0 in a box: 41-50 N, 114 to 127W
url3 = "https://prod-earthquake.cr.usgs.gov/fdsnws/event/1/query?&starttime=" + starttimestr + "&endtime=" + endtimestr + "&minlatitude=" + str(latbox1) + "&maxlatitude=" + str(latbox2) + "&minlongitude=" + str(lonbox1) + "&maxlongitude=" + str(lonbox2) + "&minmagnitude=2.0&format=text"
f3 = requests.get(url3)

# concatenate the 3 queries
lines = []
events = {}
for line in f1.iter_lines():
    linewrite = str(line).split("'")[1]
    if ( "#" not in linewrite ):
        lines.append(linewrite)
        eventtime = (linewrite.split('|')[1])
        events[eventtime] = linewrite
for line in f2.iter_lines():
    linewrite = str(line).split("'")[1]
    if ( "#" not in linewrite ):
        lines.append(linewrite)
        eventtime = (linewrite.split('|')[1])
        events[eventtime] = linewrite
for line in f3.iter_lines():
    linewrite = str(line).split("'")[1]
    if ( "#" not in linewrite ):
        lines.append(linewrite)
        eventtime = (linewrite.split('|')[1])
        events[eventtime] = linewrite

# print out the events from most recent to oldest
for event in sorted(events, reverse = True):
    line = events[event]
    print(line)

