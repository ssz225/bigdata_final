import sys
import string
import os
import numpy as np
from datetime import datetime
from sklearn import linear_model

fmt = '%Y-%m-%d %H:%M:%S'
from mrjob.job import MRJob



class Regressor(MRJob):
	
	def mapper_init(self):
		self.fitter = linear_model.SGDRegressor(loss='squared_loss', penalty='none', fit_intercept=True, random_state=None)
		weights = [float(x) for x in os.environ['weights'].split(',')]
		if weights is not None:
			self.fitter.coef_ = np.array(weights[1:])
			self.fitter.intercept_ = np.array([weights[0]])


	def mapper(self, _, line):
		#this should create a single input
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')

		p_up = datetime.strptime(items[3], fmt)
		d_time = datetime.strptime(items[6], fmt)


		minutes_worked = (d_time - p_up).total_seconds()/60.0

		#our y var
		fare_amount = float(items[-6])
		if fare_amount>0:
			#some controls
			day_of_week_flag = p_up.weekday()
			hour = p_up.hour
			#some time buckets (for hours in day)

			#fit and update the fitter
			X = np.array([[minutes_worked]])

			self.fitter = self.fitter.partial_fit(X, [fare_amount])


	def mapper_final(self):
		full_weights = list(self.fitter.intercept_) + list(self.fitter.coef_ )
		yield (1, full_weights)


	def reducer(self, key, values):
		v= [x for x in  values]
		weight_arr = list(np.mean(np.array(v), axis=0))
		yield(1, weight_arr)




if __name__ == '__main__':
    Regressor.run()
