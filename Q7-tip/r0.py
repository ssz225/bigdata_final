#!/usr/bin/python

import sys

current_key = None
current_fare = None
current_tip = None

for line in sys.stdin:
    
	key, fare, tip = line.split(",")
	try:
		fare = float(fare)
		tip = float(tip)
	except:
		continue
	#if same key, add fare, add tip
	if key == current_key:
		current_fare += fare
		current_tip += tip
	else:
	#not 1st line && diff key -> print current entry, then set current to new current
		if current_key:
			pctip = 100*(current_tip / current_fare)
			print "%s,%s" %( current_key, pctip)
		current_key = key
		current_fare = fare
		current_tip = tip
        
#print final line
pctip = 100*(current_tip / current_fare)
print "%s,%s" %( current_key, pctip )
