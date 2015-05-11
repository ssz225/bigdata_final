#!/usr/bin/python

import sys
import string

#map payment_type, count(1) for each positive tip
for line in sys.stdin:
	try:
		items = line.strip().split(",")
		if items[0] == 'medallion':
			continue
		key = items[4].upper()
		if float(items[8]) > 0:
			values = 1
		else:
			values = 0
		print '%s,%s' %(key, values)
	except:
		pass
