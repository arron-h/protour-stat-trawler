class AbstractTrawler:

	def trawlRiderStats(self, rider):
		raise NotImplementedError("AbstractTrawler: trawlRiderStats() not implemented!")

	def trawlRiderList(self, year):
		raise NotImplementedError("AbstractTrawler: trawlRiderList() not implemented!")
