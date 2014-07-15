from WikipediaTrawler import WikipediaTrawler

class TrawlerFactory:
	
	def getTrawlerForRiderList():
		# For now, just use the wikipedia trawler
		trawler = WikipediaTrawler()

		return trawler

	def getTrawlerForRiderStats(rider):
		# For now, just use the wikipedia trawler
		trawler = WikipediaTrawler()

		return trawler