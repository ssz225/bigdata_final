#!/usr/bin/python

import sys
import string

#map passenger_count and credit card payment_amount and tip_amount
for line in sys.stdin:
	try:
		items = line.strip('"').split('"\t"')
		item = items[0].split(',') + items[1].split(',')
		if len(item) == 21:
			key = item[7]
			if item[14].upper() == 'CRE':
				values = item[15]+ ',' + item[18]
				print '%s,%s' %(key, values)
	except:
		continue
