import importlib
from TrawlerTypes import TrawlerTypes
from list.WikipediaListTrawler import WikipediaListTrawler
from stats.WikipediaStatsTrawler import WikipediaStatsTrawler

class TrawlerFactory:

	@staticmethod
	def makeFriendlyTeamName(teamName):
		return teamName.translate(None, " -.")

	@staticmethod
	def getStatsTrawler(rider):
		trawlerClass = None
		try:
			trawlerName = makeFriendlyTeamName(rider.team)
			module = importlib.import_module(
				"stats."+trawlerName+"StatsTrawler")
			trawlerClass = getattr(module, trawlerName+"StatsTrawler")
			print("Using " + trawlerName + " trawler for " + rider.name)
		except:
			module = importlib.import_module("trawlers.stats.WikipediaStatsTrawler")
			trawlerClass = getattr(module, "WikipediaStatsTrawler")
			print("Using default Wikipedia trawler for " + rider.name)
		
		return trawlerClass()

	@staticmethod
	def getTrawler(type, meta=None):
		if type == TrawlerTypes.LIST:
			return WikipediaListTrawler()
		elif type == TrawlerTypes.STATS:
			return TrawlerFactory.getStatsTrawler(meta)
