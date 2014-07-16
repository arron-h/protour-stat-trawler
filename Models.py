class Rider:

	def __init__(self, name):
		self.age = None
		self.weight = None
		self.height = None
		self.name = name

	def setTrawlerData(self, data):
		self.implData = data

class Metrics:

	def __init__(self):
		self.averageWeight = 0
		self.averageHeight = 0
		self.averageAge    = 0