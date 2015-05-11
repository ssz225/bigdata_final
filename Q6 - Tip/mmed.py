#!/usr/bin/python

import sys
import string
from datetime import datetime

fmt = '%Y-%m-%d %H:%M:%S'
for line in sys.stdin:
	try:
		items = line.split(',')
		weekday = datetime.strptime((items[3]), fmt).strftime("%A")
		key = weekday
		values = items[0]
		print '%s,%s' %(key, values)
	except:
		continue
