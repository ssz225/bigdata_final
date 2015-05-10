from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from numpy import array
from datetime import datetime
import math
from pyspark.mllib.util import MLUtils
from pyspark.mllib.linalg import Vectors
import numpy as np
from numpy.linalg import inv
from pyspark.mllib.stat import Statistics


n_scaled = 1
avg_dist_fill = 2.6
n_samps = 300000

in_loc = "FILL IN"
out_loc = "FILL IN"


def get_total_seconds(td): 
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

fmt = '%Y-%m-%d %H:%M:%S'
# Load and parse the data
def parsePoint(line):
	items = line.strip('"').split('"\t"')
	items = items[0].split(',') + items[1].split(',')
	p_up = datetime.strptime(items[3], fmt)
	d_time = datetime.strptime(items[6], fmt)
	#minutes_worked = get_total_seconds(d_time - p_up)/60.0
	fare_amount = float(items[-6])
	try:
		distance = float(items[9])
	except:
		distance = avg_dist_fill
	hour_of_day = p_up.hour
	day_of_week = p_up.weekday()
	hour_dummies = [0]*23
	try:
		hour_dummies[hour_of_day] = 1
	except:
		pass
	day_dummies = [0]*6
	try:
		day_dummies[day_of_week] = 1
	except:
		pass
	month = p_up.month-1
	month_dummies = [0]*11
	try:
		month_dummies[month] = 1
	except:
		pass
	interactions = np.zeros((7,24))
	interactions[day_of_week,hour_of_day] = 1
	interactions = interactions.flatten().tolist()[:-1] #correct perfect collinearity
	X = [distance]
	X = X +  hour_dummies+  day_dummies + month_dummies + interactions
	#filter junk
	if fare_amount>0 and distance<100 and distance>0:
		return LabeledPoint(fare_amount, X)


def parseKeepD(line):
	items = line.strip('"').split('"\t"')
	items = items[0].split(',') + items[1].split(',')
	medal = items[0]
	hack = items[1]
	vendor = items[2]
	passen = items[7]
	tip = items[18]
	return parsePoint(line),[str(x) for x in [medal,hack,vendor,passen,tip]]

def conv_label_pt(lp):
	x = lp.features
	new_pt  = array(x) - array(means)
	for i in range(0,n_scaled):
		new_pt[i] = new_pt[i]/varis[i]**.5
	return LabeledPoint(lp.label, new_pt)

def std_errors(data,MSE,N):
	samp = data.takeSample(withReplacement=False, num=n_samps)
	samp = [x[0].features for x in samp]
	correction = max(1,float(N)/n_samps)
	x = np.array(samp)
	xTx_inv = inv(correction*(np.dot(x.T,x)))
	return MSE * np.diag(xTx_inv)

means = 0
varis = 0
def do_all(f_path,out_name):
	sc = SparkContext()
	data = sc.textFile(f_path)

	data = data.map(parseKeepD).filter(lambda p: p[0] != None)

	# Scale Features
	features = data.map(lambda x: x[0].features)
	summary = Statistics.colStats(features)
	global means
	global varis
	means = summary.mean()
	varis = summary.variance()

	#scale the points
	data = data.map(lambda y: (conv_label_pt(y[0]),y[1]))

	#train model
	model = LinearRegressionWithSGD().train(data.map(lambda x: x[0]), intercept=True, regType='none')

	#calculate disparity
	disparity = data.map(lambda p: (p[0].label, model.predict(p[0].features), p[1]))  

	#calculate SSR for later
	ssr = disparity.map(lambda x: (x[0] - x[1])**2).sum()

	#keep N
	N = disparity.count()
	#shut down SC
	MSE = ssr/float(N)
	se = std_errors(data,MSE,N)
	disparity.saveAsTextFile(out_loc + out_name)

	sc.stop()
	return model.intercept,model.weights,se,disparity, ssr, N

i_1,w_1,w_1e,disp_1,ssr1,N1 = do_all(in_loc + "2010/","2010")

i_2,w_2,w_2e,disp_2,ssr2,N2 = do_all(in_loc + "2013/","2013")

i_c,w_c,w_ce,disp_c,ssrC,NC = do_all(in_loc + "C/","Combined")


def do_chow(ssr_1,ssr_2, ssr_c, N1,N2):
	#chow test for equality
	k = len(w_1) + 1
	chow_stat = float(((ssr_c - (ssr_1 + ssr_2))/float(k)))/((ssr_1 + ssr_2)/(N1 + N2 - 2*k))
	return chow_stat, (k, N1 + N2 - 2*k)


def z_test(w1,w2,s1,s2):
	z_s = np.zeros(len(w1))
	for i in range(0,len(w1)):
		z_s[i] = (w1[i] - w2[i])/((abs(s1[i])**.5 + abs(s2[i])**.5)**.5)
	return z_s


c_stats,F = do_chow(ssr1,ssr2,ssrC,N1,N2)

print c_stats,F

print i_1
print w_1
print w_1e


print i_2
print w_2
print w_2e

print z_test(w_1,w_2,w_1e,w_2e)

