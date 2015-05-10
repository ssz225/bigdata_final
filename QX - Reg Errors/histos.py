import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import json

f_2010 = glob.glob('outputs/2010/p*')

f_2013 = glob.glob('outputs/2013/p*')

def file_loop(f):
    lines = [line.strip().split('\t') for line in open(f)]
    vals = [(l[0],json.loads(l[1])[0],json.loads(l[1])[1] )for l in lines]
    return vals

v_2010 = []
for f in f_2010:
    v_2010.extend(file_loop(f))


v_2013 = []
for f in f_2013:
    v_2013.extend(file_loop(f))

def make_graph(values, label):
	n, bins, patches = plt.hist(values, 35, normed=1, stacked=1,facecolor='green', alpha=0.75)
	# add a 'best fit' line (assuming normality)
	y = mlab.normpdf( bins, np.mean(values), np.std(values))
	l = plt.plot(bins, y, 'r--', linewidth=1)

	plt.xlabel(label)
	plt.ylabel('Scaled Frequency')
	plt.title(r'Distribition of ?' + label)
	#plt.axis([.1, .9,0,10])
	plt.grid(True)

	plt.savefig(label + '.png', dpi=400)
	plt.close()

#strip teh very strange outliers
avg_err_10 = [v[1] for v in v_2010 if (x<1 and x>-1)]
abs_err_10 = [v[2] for v in v_2010 if (x<50 and x>50)]

avg_err_13 = [v[1] for v in v_2013 if (x<1 and x>-1)]
abs_err_13 = [v[2] for v in v_2010 if (x<50 and x>50)]

make_graph(avg_err_10, 'Average Errors 2010')
make_graph(abs_err_10, 'Absolute Errors 2010')
make_graph(avg_err_13, 'Average Errors 2013')
make_graph(avg_err_13, 'Absolute Errors 2013')