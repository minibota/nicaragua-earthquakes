#!/usr/bin/env python
#coding=utf-8

import ssl
import re
import urllib2
from BeautifulSoup import BeautifulSoup

URL = 'https://165.98.224.55/geofisica/sis/events/sismos.php'
FILENAME = 'quakes-ni.csv'

try:
	ssl._create_default_https_context = ssl._create_unverified_context
	# parse html
	page = urllib2.urlopen(URL, timeout=30)
	soup = BeautifulSoup(page)
	x = soup.findAll('pre')
	
	open(FILENAME, 'w').close() # reset file
	titles = "date,time,latitude,longitude,depth,magnitude,location,country"
	with open(FILENAME, 'w+') as f:
		print >>f, titles
		for p in x:
			p = p.text.encode('utf-8')

			p = re.sub(r'(.*[0-9])[A-Z]([0-9].*)', r'\1 \2', p) # Skip 'C' character
			print p
			l = re.sub(r'\s+', ' ', p).split(' ') # remove spaces and convert to array
			if len(l) == 1:
				continue
			
			location = ' '.join(l[6:])
			l = l[0:6]
			l[2] = l[2][0:-1]
			l[3] = '-' + l[3][0:-1]
			
			#l[5] = l[5][0:-2] # skip 'ML' or 'MC'
			#l[5] = l[5][0:-1] # skip 'C'
			
			l.append(location)
			l = ",".join(l) # convert to csv
			print >>f, l
except urllib2.URLError, e:
	print e
	print 'TIMEOUT, Try again'
