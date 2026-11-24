#!/usr/bin/env python3

import urllib.request
import json
import sys

try:
    j = urllib.request.urlopen('http://api.pioupiou.fr/v1/live/503', timeout=30)
    m = json.load(j)['data']['measurements']
    fields = ('wind_heading', 'wind_speed_avg', 'wind_speed_max', 'wind_speed_min', 'date')
    values = [m[f] for f in fields]
except (OSError, ValueError, KeyError, TypeError) as e:
    sys.exit('Error: failed to get wind data: %s: %s' % (type(e).__name__, e))

missing = [f for f, v in zip(fields, values) if v is None]
if missing:
    sys.exit('Error: sensor reported no data for: %s' % ', '.join(missing))

print('Wind direction %s, speed %s km/h, max %s km/h, min %s km/h. Taken %s' % tuple(values))
