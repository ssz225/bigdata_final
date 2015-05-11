#!/usr/bin/python

import sys

current_key = None
current_value = 1
total_value = 1

for line in sys.stdin:
    
	key, value = line.split(",")
	try:
		value = float(value)
	except:
		continue
	#if same key, add fare, add tip
	if key == current_key:
		current_value = current_value + value
		total_value = total_value + 1
	else:
	#not 1st line && diff key -> print current entry, then set current to new current
		if current_key:
			pctip = 100*(current_value / total_value)
			print "%s,%s" %( current_key, pctip)
		current_key = key
		current_value = value
		total_value = 1
        
#print final line
pctip = 100*(current_value / total_value)
print "%s,%s" %( current_key, pctip )
