import sys
import string
import os
import numpy as np
from datetime import datetime

fmt = '%Y-%m-%d %H:%M:%S'
from mrjob.job import MRJob

class HotHand(MRJob):

	def mapper(self, _, line):
		#take all csv objects
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')

		medallion = items[0]
		pickup_day=items[3]
		tips = float(items[-3])
		#all - tip
		rev = float(items[-1]) - tips
		try:
			tip_per = float(tips)/rev 
		except:
			tip_per = 0

		yield (medallion, [pickup_day, tip_per])
			

	def reducer(self, key, values):
		values = sorted(values, key=lambda x: datetime.strptime(x[0], fmt))
		#this controls for possible time trend in data
		medians_dict = dict()
		for v in values:
			p_d = datetime.strptime(v[0], fmt).date()
			if p_d in medians_dict:
				medians_dict[p_d].append(v[1])
			else:
				medians_dict[p_d] = [v[1]]
		for day in medians_dict:
			medians_dict[day] = np.median([x for x in medians_dict[day] if x> 0 ])

		up_up = 0
		up_down = 0
		for i in range(0,len(values)-1):
			time, tip = values[i]
			day = datetime.strptime(time, fmt).date()
			time_plus1, tip_plus1 =values[i+1]
			day_plus1 = datetime.strptime(time_plus1, fmt).date()
			if ((tip > 0) and (tip_plus1 >0) and (tip> medians_dict[day]) and (day == day_plus1)):
				if tip_plus1 > medians_dict[day]:
					up_up +=1
				else:
					up_down +=1
		try:	
			out_var = float(up_up)/(up_up + up_down)
		except:
			out_var = np.nan
		yield (key, out_var)

if __name__ == '__main__':
    HotHand.run()