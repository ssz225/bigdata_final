import sys
import string
import os


from mrjob.job import MRJob


class RegErrors(MRJob):

	def mapper(self, _, line):
		x = line.strip('"(').split(",")[:4]
		actual,pred = [float(a) for a in x[:2]]
		m1 = x[2].strip('"[').strip('" [').strip('\'')
		m2 = x[3].strip('"[').strip('" [').strip('\'')
		driver = m1 + "_" + m2
		yield (driver, [actual,pred])


	def reducer(self, key, values):
		vals = [v for v in values]
		percs = []
		absos = []
		for v in vals:
			try:
				percs.append(float(v[0] - v[1]) / v[1])
			except:
				pass
			try:
				absos.append(float(v[0] - v[1]))
			except:
				pass
		yield (key, [float(sum(percs))/len(percs), float(sum(absos))/len(absos)])

if __name__ == '__main__':
    RegErrors.run()