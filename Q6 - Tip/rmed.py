#!/usr/bin/python

import sys

current_key = None
current_med = None

for line in sys.stdin:
    
	key, med = line.strip().split(",")
	#if same key, add fare, add tip
	if key == current_key:
		if med != current_med:
			sum = sum + 1
			current_med = med
		else:
			continue
	else:
	#not 1st line && diff key -> print current entry, then set current to new current
		if current_key:
			print "%s,%s" %( current_key, sum)
		current_key = key
		current_med = med
		sum = 1
        
#print final line
print "%s,%s" %( current_key, sum )
