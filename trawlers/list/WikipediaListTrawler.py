import os, re, urllib2, sys
from AbstractListTrawler import AbstractListTrawler
from Models import Rider
from trawlers.sites.Wikipedia import Wikipedia

class WikipediaListTrawler(AbstractListTrawler):

	def _buildRiderList(self, year):
		response  = None
		riders    = []
		countries = {}

		try:
			response = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_"+
				str(year)+"_UCI_ProTeams_and_riders")
		except:
			raise IOError("Failed to open the url to Wikipedia.")

		html = response.read()

		prog    = re.compile("<a href=\"(.*?)\"[^>]*>(.*?)</a>&#160;<span style=\"font-size:90%;\">\(<abbr title=\"(.*?)\">([A-Z]{3})</abbr>\)</span></td>")
		matches = prog.findall(html)

		# Grab riders
		for match in matches:
			rider = Rider(match[1])

			wikiData = {}
			wikiData["cache"] = Wikipedia.buildSafeCacheFilename(match[0])
			wikiData["url"]   = Wikipedia.baseUrl + match[0]

			rider.setTrawlerData(wikiData)

			# Grab country name
			countryId   = match[3]
			countryName = match[2]
			if not countryId in countries:
				countries[countryId] = countryName

			rider.country = countryId

			riders.append(rider)

		return (riders, countries)

	def trawl(self, year):
		return self._buildRiderList(year)