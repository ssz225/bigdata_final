from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from numpy import array
from datetime import datetime

def get_total_seconds(td): 
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

fmt = '%Y-%m-%d %H:%M:%S'
# Load and parse the data
def parsePoint(line):
	items = line.strip('"').split('"\t"')
	items = items[0].split(',') + items[1].split(',')
	p_up = datetime.strptime(items[3], fmt)
	d_time = datetime.strptime(items[6], fmt)
	minutes_worked = get_total_seconds(d_time - p_up)/60.0
	fare_amount = float(items[-6])
	X = [minutes_worked]
	return LabeledPoint(fare_amount, X)

data = sc.textFile("s3n://AWS_ACCESS_KEY_ID:AWS_SECRET_KEY@trip-fare-join/2010/")
parsedData = data.map(parsePoint)

# Build the model
model = LinearRegressionWithSGD.train(parsedData)

# Evaluate the model on training data
valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
print("Mean Squared Error = " + str(MSE))


