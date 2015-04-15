import sys
import string
import os
from datetime import datetime

fmt = '%Y-%m-%d %H:%M:%S'
from mrjob.job import MRJob

class HoursWorked(MRJob):

	def mapper(self, _, line):
		#take all csv objects
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')
		#datetimeify the fields
		p_up = datetime.strptime(items[3], fmt)
		d_time = datetime.strptime(items[6], fmt)
		#no minutes attribute (go figure)
		minutes_worked = (d_time - p_up).total_seconds()/60.0
		#we'll tag this entry with the day (from pickup)
		medallion = items[0]
		pickup_day = p_up.date().__str__()

		#rev numbers
		#floatify end of list
		rev = sum([float(items[-6]),float(items[-5]),float(items[-3]),float(items[-2])])

		yield (medallion, [pickup_day, minutes_worked, rev])

	def combiner(self, key, values):
		sum_dict = dict()
		for v in values:
			pickup_day = v[0]
			if pickup_day in sum_dict:
				sum_dict[pickup_day][0] += v[1]
				sum_dict[pickup_day][1] += v[2]
			else:
				sum_dict[pickup_day] = v[1:]
		out_val = []
		for k, v in sum_dict.iteritems():
			yield(key, [k] + v)
			

	def reducer(self, key, values):
		sum_dict = dict()
		for v in values:
			pickup_day = v[0]
			if pickup_day in sum_dict:
				sum_dict[pickup_day][0] += v[1]
				sum_dict[pickup_day][1] += v[2]
			else:
				sum_dict[pickup_day] = v[1:]
		minutes = []
		revs = []
		for v in sum_dict.values():
			minutes.append(v[0])
			revs.append(v[1])
		out = [sum(minutes)/ float(len(minutes)), sum(revs)/ float(len(revs))]
		yield (key, out)

if __name__ == '__main__':
    HoursWorked.run()