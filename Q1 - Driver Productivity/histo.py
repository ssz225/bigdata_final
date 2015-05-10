import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


in_files = glob.glob('output-2010/p*')

def file_loop(f):
    lines = [line.strip().split('\t') for line in open(f)]
    vals = [l[1] for l in lines ]
    vals = [v.strip('[]\'').split(",") for v in vals]
    return [[float(a), float(b)] for (a,b) in vals]

all_vals =[]
for f in in_files:
    all_vals.extend(file_loop(f))

#drop nonsense values where revenues are negative/ more minutes than minutes in a workday

all_vals = [a for a in all_vals if (a[1]>0 and a[0]<1440) ]

minutes = [a[0] for a in all_vals]
revs = [a[1] for a in all_vals]

#chart revs vs minutes
plt.scatter(minutes, revs, alpha=0.5)
plt.title(r'Revenue vs Minutes Worked')
plt.grid(True)
plt.xlabel('Minutes Worked/Day')
plt.ylabel('Daily Revenue')
plt.savefig('Minutes_v_Rev.png', dpi=400)
plt.close()

