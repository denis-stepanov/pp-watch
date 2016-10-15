#!/usr/bin/python

import urllib2
import json

j = urllib2.urlopen('http://api.pioupiou.fr/v1/live/503')
j_obj = json.load(j)

#print json.dumps(j_obj, indent=4, sort_keys=True)

print 'Wind direction %s, speed %s km/h, max %s km/h, min %s km/h. Taken %s' % (j_obj['data']['measurements']['wind_heading'], j_obj['data']['measurements']['wind_speed_avg'], j_obj['data']['measurements']['wind_speed_max'], j_obj['data']['measurements']['wind_speed_min'], j_obj['data']['measurements']['date'])
