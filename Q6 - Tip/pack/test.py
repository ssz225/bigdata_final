import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

taxi = pd.read_csv('pyutaxi.csv')
tip = pd.read_csv('pytipday.csv')
tiptaxi = tip.merge(taxi, on='day')
tiptaxi.to_csv('tiptaxi.csv', index=False)
tiptaxi = pd.DataFrame(pd.read_csv('tiptaxi.csv'))
tiptaxi['ratio'] = tiptaxi['tip']/tiptaxi['taxi']
print tiptaxi
tiptaxi.to_csv('tiptaxi.csv', index=False)

tiptaxi.plot(kind='line', x='day', y='ratio')
plt.title('Tips Per Taxi By Day')
plt.xlabel('Day')
plt.ylabel('Tips Earned ($)')
plt.savefig('tips_per_taxi.pdf')
plt.show()
# f=open('tiptaxi.csv','r')
# line = f.readlines
# for l in line:
#     day, ntip, ntaxi = line.strip().split(",")
#     ntip = float(ntip)
#     ntaxi = float(ntaxi)
#     ratio = ntip/ntaxi
#     print "%s,%d" %(day, ratio)
    
# tiptaxi = pd.read_csv('tiptaxi.csv')
# ratio = tiptaxi[1]/tiptaxi[3]
# print ratio
# for line in tiptaxi:
#     day, ntip, index, ntaxi = line.strip().split(",")
#     ntip = float(ntip)
#     ntaxi = float(ntaxi)
#     ratio = ntip/ntaxi
#     print "%s,%d" %(day, ratio)