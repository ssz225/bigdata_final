import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

in_files = glob.glob('q6-output/p*')

def file_loop(f):
    lines = [line.strip().split('\t') for line in open(f)]
    vals = [float(l[1]) for l in lines if str(l[1]) != 'NaN' ]
    return vals


all_vals =[]
for f in in_files:
    all_vals.extend(file_loop(f))


n, bins, patches = plt.hist(all_vals, 35, normed=1, stacked=1,facecolor='green', alpha=0.75)

# add a 'best fit' line (assuming normality)
y = mlab.normpdf( bins, np.mean(all_vals), np.std(all_vals))
l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('P(tip(t+1)>median) | tip(t)>median)')
plt.ylabel('Scaled Frequency')
plt.title(r'Are Good Tips Followed by Good Tips?')
plt.axis([.1, .9,0,10])
plt.grid(True)

plt.savefig('Histogram.png', dpi=400)