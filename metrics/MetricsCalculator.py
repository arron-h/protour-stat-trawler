import operator

class MetricsCalculator:

	def __init__(self):
		self._counts = { 
			"weight": 0,
			"height": 0,
			"age": 0
		}
		self._totals = { 
			"weight": 0,
			"height": 0,
			"age": 0
		}
		self._countryTotals = {}

	def recalculate(self, metrics, rider):
		if rider.weight:
			self._counts["weight"] += 1
			self._totals["weight"] += float(rider.weight)

		if rider.height:
			self._counts["height"] += 1
			self._totals["height"] += float(rider.height)

		if rider.age:
			self._counts["age"] += 1
			self._totals["age"] += int(rider.age)

		if self._counts["weight"]:
			metrics.averageWeight = self._totals["weight"] / self._counts["weight"]

		if self._counts["height"]:
			metrics.averageHeight = self._totals["height"] / self._counts["height"]

		if self._counts["age"]:
			metrics.averageAge    = self._totals["age"]    / self._counts["age"]

		if rider.country:
			# Initialise the totals if the key doesn't exist
			if not rider.country in self._countryTotals:
				self._countryTotals[rider.country] = 0

			self._countryTotals[rider.country] += 1

	def performPostCalculations(self, metrics):
		# Sort the dict to return a list of kv tuples
		s = sorted(self._countryTotals.iteritems(), key=operator.itemgetter(1))
		s.reverse()
		
		metrics.countryRep = s[0][0]
		metrics.countryRepCount = s[0][1]
