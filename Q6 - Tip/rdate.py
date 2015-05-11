#!/usr/bin/python

import sys

current_key = None
current_tip = None

for line in sys.stdin:
    
	key, tip = line.strip().split(",")
	try:
		tip = float(tip)
	except ValueError:
		continue
	#if same key, add fare, add tip
	if key == current_key:
		current_tip += tip
	else:
	#not 1st line && diff key -> print current entry, then set current to new current
		if current_key:
			print "%s,%s" %( current_key, current_tip)
		current_key = key
		current_tip = tip
        
#print final line
print "%s,%s" %( current_key, current_tip )
