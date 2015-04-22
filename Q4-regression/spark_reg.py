from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from numpy import array

# Load and parse the data
def parsePoint(line):
		items = line.strip('"').split('"\t"')
		items = items[0].split(',') + items[1].split(',')

		p_up = datetime.strptime(items[3], fmt)
		d_time = datetime.strptime(items[6], fmt)


		minutes_worked = (d_time - p_up).total_seconds()/60.0

		#our y var
		fare_amount = float(items[-6])
		if (fare_amount>0 and minutes_worked<1440):
			#some controls
			day_of_week_flag = p_up.weekday()
			hour = p_up.hour
			#some time buckets (for hours in day)

			#fit and update the fitter
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


