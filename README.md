Earliest arrival times of recent regional and teleseismic earthquakes at the PNSN using the <a href="https://earthquake.usgs.gov/fdsnws/event/1">NEIC event web service</a> . Times shown are for the earliest P arrival to the closest of a series of 9 points outlining the WA & OR borders . First arrival times for regional (e.g. CA, Vancouver Island) events can vary by a few seconds from the reference location, for farther earthquakes, arrival times will vary less and less as distance increases.  For travel times, a precalculated travel time file is used that covers every distance and depth event by linearly interpolating travel times.

**Example output**

Most recent earthquake arrivals at PNSN: <a href="https://seismo.ess.washington.edu/ahutko/recent_events.txt">recent_events.txt</a>
<pre>
Version:   Mon Sep 21 15:10:02 PDT 2020
           Mon Sep 21 22:10:02 UTC 2020
 
arrival @PNSN (UTC)      Mag     Dep   Dist   Lat    Lon     Location
                                 (km) (deg)
2020-09-21 20:30:13    mb,4.1,us  108    74  -18.5   -69.9   Arica, Chile
2020-09-21 20:12:09    mb,4.4,us   10    98   26.3    91.3   H\xc4\x81jo, India
2020-09-21 18:55:54    ml,2.4,us   12     1   44.1  -115.1   Stanley, Idaho
2020-09-21 18:31:15    mb,4.6,us   10    71   51.8   103.5   Kultuk, Russia
...
</pre>

**Requiremets**

python with packages: obspy ( for obspy.geodetics.locations2degrees), requests

**Earthquakes listed**

M ≥ 4.0 global

M ≥ 3.0 within 15* radius of Yakima (center of PNSN)

M ≥ 2.0 within ~2* of WA/OR border

File is currently generated on monitor as user:seis on a crontab every 2 minutes on even minutes and relies on the NEIC comcat webservice.  Results are rsynced to a public webpage.

**Files**

-*get_events.py:*  performs the NEIC comcat queries.  Configure your network's boundaries/event thresholds here.

-*get_travel_times.py:*  reads output of get_events.py and spits out a text file of arrival times at the (kinda) closest point in the network

-*generate_recent_events.csh:*  runs *get_events.py* and *get_travel_times.py* on a cronjob to generate the final output to be published, *recent_events*.  Twice a day it looks back for an entire week, then at all other times it just looks back on the current day to keep it light weight and fast.

-*TT.iasp91:* first arrival tavel times at every degree for events with depths ( 0, 10, 20, 30, 35, 40, 50, 70, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700 km).  Transition from Pdiff to PKP is at a conservative 115 degrees.

-*today_events/older_events:* text file output of get_events.py used in the cron script.

-*recent_events:* text file that gets rsynced to webpage for seismologists' viewing pleasure.
