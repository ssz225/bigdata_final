#!/usr/bin/python

import sys
import string

for line in sys.stdin:
	try:
		items = line.strip().split(",")
		if items[0] == 'medallion':
			continue
		key = items[4].upper()
		if float(items[8]) > 0:
			values = items[5] + "," + items[8]
			print '%s,%s' %(key, values)
	except:
		pass
