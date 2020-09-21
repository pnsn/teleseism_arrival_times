#!/bin/csh

set d = `date`
set dutc = `date -u`
set hour = `date -u +%-H`
set minute = `date -u +%-M`

cd ~/TELESEISM_ARRIVAL_TIMES

/bin/rm junk?

if ( ( $hour == 0 || $hour == 1 ) && $minute == 0 ) then
    #---- get all events from past week up until today 00:00:00 UTC (usually a longer list --> slower)
    ./get_events.py -d 7 >! events_Fetched
    ./get_travel_times.py >! junk
    sort -ru junk | sed '/^$/d' >! older_events
else
    #---- only get today's (UTC) events (usually a short list --> faster)
    ./get_events.py -d 0 >! events_Fetched
    ./get_travel_times.py >! junk
    sort -ru junk | sed '/^$/d' >! today_events
endif

echo ' ' >! recent_events
echo 'Version:  ' $d >> recent_events
echo '          ' $dutc >> recent_events
echo ' ' >> recent_events
echo "arrival @PNSN (UTC)      Mag     Dep   Dist   Lat    Lon     Location" >> recent_events
echo "                                 (km) (deg)" >> recent_events
cat today_events >> recent_events
cat older_events >> recent_events

# rsync to webpage

