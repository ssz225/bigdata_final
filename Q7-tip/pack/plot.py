import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#passenger plot
passenger = pd.DataFrame(pd.read_csv('pass.csv'))
plot = passenger.plot(kind='bar', x='pass',  y='pctip')
plt.title('Credit Card Tip Percentage vs Passenger Count')
plt.xlabel('Number of Passengers')
plt.ylabel('Percentage')
plt.savefig('tip_passenger.pdf')
plt.show()

a = pd.read_csv("pc0.csv")
b = pd.read_csv("pyno0.csv")
ct = pd.read_csv("pyct.csv")

#ct
ct.plot(kind='line', x='type', y='pcct', label = 'Tipped Rides/Total Rides', color='black')
plt.xlabel('Payment Type')
plt.ylabel('Percentage')
plt.legend(loc = 'upper right')
plt.title('Ratio of Tipped Rides vs Total Rides by Payment Type')
plt.savefig('pct.pdf')
plt.show()

#0, no0
merged = a.merge(ct, on='type')
merged.to_csv("pcmerge.csv", index=False)
pcm = pd.read_csv('pcmerge.csv')
pcm.plot(kind='line', x = 'type', y='pcct', label='Tipped Rides/Total Rides', color = 'black')
pcm.plot(kind='line', x='type', y='pc', label='Tip By Type', color ='b')
plt.xlabel('Payment Type')
plt.ylabel('Percentage')
plt.legend(loc = 'upper right')
plt.savefig('pct_pc0.pdf')
plt.show()

#ct, 0, no0
mct = pcm.merge(b, on='type')
mct.to_csv("pctmerge.csv", index=False)
mctp = pd.read_csv("pctmerge.csv")
mctp.plot(kind='line', x='type', y='pcct', label = 'Tipped Rides/Total Rides', color = 'black')
mctp.plot(kind='line', x = 'type', y='pc', label = 'Tip By Type', color = 'b')
mctp.plot(kind='line', x='type', y='pcno0', label = 'Tip By Type (Removed 0s)', color = 'g')
plt.xlabel('Payment Type')
plt.ylabel('Percentage')
plt.legend(loc = 'upper right')
plt.savefig('pct_pc0_pcno0.pdf')
plt.show()

#tip per day
tip = pd.read_csv('pytipday.csv')
tip.plot(kind='line', x='day', y='tip', color='r')
plt.title('Total Tips Per Day')
plt.xlabel('Day')
plt.ylabel('Amount of Tips ($M)')
plt.savefig('total_tip.pdf')
plt.show()

#number unique taxi per day
taxi = pd.read_csv('pyutaxi.csv')
taxi.plot(kind='line', x='day', y='taxi', color='b')
plt.title('Number of Unique Taxis Per Day')
plt.xlabel('Day')
plt.ylabel('Number of Taxis')
plt.savefig('total_taxis.pdf')
plt.show()

#Tips per taxi per day
tiptaxi = tip.merge(taxi, on='day')
tiptaxi.to_csv('tiptaxi.csv', index=False)
tiptaxi = pd.DataFrame(pd.read_csv('tiptaxi.csv'))
tiptaxi['ratio'] = tiptaxi['tip']/tiptaxi['taxi']
tiptaxi.to_csv('tiptaxi.csv', index=False)
tiptaxi.plot(kind='line', x='day', y='ratio')
plt.title('Tips Per Taxi By Day')
plt.xlabel('Day')
plt.ylabel('Tips Earned ($)')
plt.savefig('tips_per_taxi.pdf')
plt.show()