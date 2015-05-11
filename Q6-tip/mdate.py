#!/usr/bin/python

import sys
import string
from datetime import datetime

#map day, tip_amount
fmt = '%Y-%m-%d %H:%M:%S'
for line in sys.stdin:
	try:
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')
		weekday = datetime.strptime((items[3]), fmt).strftime("%A")
		if len(items) == 21:
			key = weekday
			values = items[18]
			print '%s,%s' %(key, values)
	except:
		continue
