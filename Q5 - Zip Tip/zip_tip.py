import sys
import string
import os
import numpy as np
import cPickle as pickle

from mrjob.job import MRJob
m = pickle.load(open("zip_grid.p","rb"))

class ZipTip(MRJob):

	def mapper(self, _, line):
		def return_zip(lat, lon, nw_lat=40.917, nw_lon=-74.260, steps=0.002):
		    try:
		    	lat, lon = float(lat), float(lon)     
		    	i, j = int((nw_lat - lat)/steps), int((lon - nw_lon)/steps)
		        return m[i][j]
		    except:
		        return -1
		#take all csv objects
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')

		lon,lat = tuple([x for x in items[12:14]])
		#some seem to be transposed
		zip_c = max(return_zip(lat,lon), return_zip(lon,lat))
		tips = float(items[-3])
		#all - tip
		rev = float(items[-1]) - tips
		try:
			tip_per = float(tips)/rev 
		except:
			tip_per = 0
		if tip_per > 0:
			yield (str(zip_c), float(tip_per))


	def reducer(self, key, values):
		tips = [v for v in values]
		count = len(tips)
		avg_tip = sum(tips)/float(len(tips))
		yield (key, [avg_tip, count])

if __name__ == '__main__':
    ZipTip.run()