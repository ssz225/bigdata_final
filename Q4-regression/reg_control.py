import sys
import string
import os
import numpy as np
import subprocess
import re

weights = [10,10]


def make_run(weights):
	part_1 = 'python regression.py -r local --cmdenv weights='
	weight_str = ','.join([str(w) for w in weights])
	part_2 = ' test_inputs/'
	return part_1 + weight_str + part_2

diff = 100
tolerance = 10**-5

while diff > tolerance:
	run_str = make_run(weights)
	last_weights = np.array(weights)
	p = subprocess.Popen(run_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	x= p.stdout.readlines()
	for i in range(0,len(x)):
		if re.match('Streaming final output from', x[i]):
			weights = [float(y) for y in x[i+1].strip('1\t\'[\]\n').split(',')]
	#l2 
	print weights
	diff = np.linalg.norm(np.array(weights) - last_weights, 2)

