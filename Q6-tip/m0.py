#!/usr/bin/python

import sys
import string

#map payment_type, fare_amount, tip_amount
for line in sys.stdin:
	try:
		items = line.strip().split(",")
		if items[0] == 'medallion':
			continue
		key = items[4].upper()
		values = items[5] + "," + items[8]
		print '%s,%s' %(key, values)
	except:
		continue
