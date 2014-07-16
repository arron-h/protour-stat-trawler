from TrawlerTypes import TrawlerTypes
from list.WikipediaListTrawler import WikipediaListTrawler
from stats.WikipediaStatsTrawler import WikipediaStatsTrawler

class TrawlerFactory:
	
	@staticmethod
	def getTrawler(type):
		if type == TrawlerTypes.LIST:
			return WikipediaListTrawler()
		elif type == TrawlerTypes.STATS:
			return WikipediaStatsTrawler()