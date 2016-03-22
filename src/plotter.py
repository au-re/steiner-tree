import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from pymongo import MongoClient

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')

db = client.steiner
results = db.results

baseline = {
	"MaxFitness": 1000,
	"PopSize": 100,
	"CrossProb": 0.9,
	"MutProb": 0.05,
	"TournSize": 20,
	"NumberGen": 100,
	"CompCost": 50,
	"Mu": 30
}

label_values = [] # AvgComponents [1.1, 1.2] per label
labels = [] # pop 100, pop 500

for label in results.distinct('PopSize'):
	
	label_value = []
	
	baseline['PopSize'] = label
	labels.append(label)
	
	print(baseline)
	
	for res in results.find(baseline):
		print(res)
		label_value.append(res['AvgComponents'])
	
	label_values.append(label_value)
	
print (label_values)
	
# find all population 100 with the baseline	
'''
class Point:
	
	def __init__(self, weights=None, components=None, value=0):
		
			Represent one tested value (e.g. population size) against 
			the number of components in the tree
		
			Attribute
			weights - array containing the weights (from the different runs) 
			components - array of component numbers (from the different runs)
			value - value to plot the point against (e.g. population 50)
		
		
		
		self.components = components
		self.weights = weights
		self.value = value
'''		

class ResultPlot:
	
	def __init__(self, label_name, label_values, labels):
		
		self.label_name = label_name
		self.label_values = label_values
		self.labels = labels
		
	def plot(self):
		
		# self.points = [Point(components=[2,3,4], value=50),Point(components=[5,6,7], value=100),Point(components=[-1,0,1], value=200)]
		#self.label_values = [point.value for point in self.points]
		
		plt.xlabel(self.label_name)
		plt.ylabel('components')
		
		component_boxes = []
		
		# for point in self.points:
		box = plt.boxplot(label_values, vert=True, labels=self.labels, patch_artist=True)
		
		for patch in box['boxes']:
			patch.set_facecolor('pink')
			
		plt.savefig('./plots/' + self.label_name + '_components.png')
		plt.clf()
		
		
rp = ResultPlot('PopSize', label_values, labels)
rp.plot()
		
	
		
		