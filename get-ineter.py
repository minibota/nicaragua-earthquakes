#!/usr/bin/env python
#coding=utf-8

import re
import urllib2
from BeautifulSoup import BeautifulSoup

URL = 'http://165.98.224.55/geofisica/sis/events/sismos.php'
FILENAME = 'quakes-ni.csv'

try:
	# parse html
	page = urllib2.urlopen(URL, timeout=30)
	soup = BeautifulSoup(page)
	x = soup.findAll('pre')
	
	open(FILENAME, 'w').close() # reset file
	titles = "date,time,latitude,longitude,depth,magnitude,location"
	with open(FILENAME, 'w+') as f:
		print >>f, titles
		for p in x:
			p = p.text.encode('utf-8')
			l = re.sub(r'\s+', ' ', p).split(' ') # remove spaces and convert to array
			location = ' '.join(l[6:])
			l = l[0:6]
			l[2] = l[2][0:-1]
			l[3] = '-' + l[3][0:-1]
			l[5] = l[5][0:-2] # skip 'ML' or 'MC'
			l.append(location)
			l = ",".join(l) # convert to csv
			print >>f, l
except urllib2.URLError, e:
	print 'TIMEOUT, Try again'
