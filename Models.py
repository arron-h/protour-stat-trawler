class Rider:

	def __init__(self, name):
		self.age = 0
		self.weight = 0
		self.height = 0
		self.name = name
		self.country = None
		self.team = None

	def setTrawlerData(self, data):
		self.implData = data

class Metrics:

	def __init__(self):
		self.averageWeight = 0
		self.averageHeight = 0
		self.averageAge    = 0