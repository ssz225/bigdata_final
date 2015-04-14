import sys
import string
import os
from mrjob.job import MRJob

class MRTripFareJoin(MRJob):

	def mapper(self, _, line):
		keys = ['medallion', 'hack_license', 'vendor_id','pickup_datetime']
		trips_key_inds = [0,1,2,5]
		fares_key_inds = [0,1,2,3]
		file_name = os.environ['map_input_file']

		l = line.strip().split(',')
		if l[0] == 'medallion':
			pass
		else:
			if file_name.find('trip_data')>-1:
			    key_inds = trips_key_inds
			else:
			    key_inds = fares_key_inds
			key_vals = [l[k] for k in key_inds]
			key = ",".join(key_vals)
			vals = [file_name]
			for i in range(len(l)):
				if not(i in key_inds):
					vals.append(l[i])
			values = ",".join(vals)
			#print values
			yield (key, values) 

	def reducer(self, key, values):
		trip_vals = []
		fare_vals = []
		for v in values:
			v = v.split(',')
			file_type = v[0]
			if file_type.find('trip_data')>-1:
				trip_vals.append(v[1:])
			else:
				fare_vals.append(v[1:])
		out_combs = [x + y for x in trip_vals for y in fare_vals]
		for out in out_combs:
		    val = ",".join(out)
		    yield (key, val) 

if __name__ == '__main__':
    MRTripFareJoin.run()