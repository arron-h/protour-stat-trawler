import os, re, urllib2, sys
from unidecode import unidecode
from AbstractStatsTrawler import AbstractStatsTrawler
from Models import Rider

weightRx   = re.compile("<span class=\"labeled\">Weight:</span> ([0-9\.]+)\s?kg")
heightRx   = re.compile("<span class=\"labeled\">Height:</span> ([0-9\.]+)\s?m")
ageRx      = re.compile("<span class=\"labeled\">Date of birth:</span> [0-9]{2}/[0-9]{2}/[0-9]{4}<span> \(([0-9]+) years old\)</span>")

class TeamEuropcarStatsTrawler(AbstractStatsTrawler):

	def __init__(self):
		self.bioUrl   = "http://www.teameuropcar.com/en/fiche-coureur/"

		AbstractStatsTrawler.__init__(self)

	def getName(self):
		return "TeamEuropcar"	

	def _matchRegEx(self, regex, html, desc):
		m = regex.search(html)
		if m:
			return m.group(1)

		return 0

	def _parseRiderHtml(self, rider, html):
		rider.weight = self._matchRegEx(weightRx, html, "weight")
		rider.height = self._matchRegEx(heightRx, html, "height")
		rider.age    = self._matchRegEx(ageRx,    html, "age")

	def _getRiderStats(self, rider):
		html = self._tryLoadRiderFromCache(rider)

		if not html:
			response = None
			try:
				riderNames = rider.name.split(" ")
				url        = self.bioUrl
				for nameComp in riderNames:
					url = url + unidecode(unicode(nameComp, "utf_8")) + "-"

				url = url.rstrip("-") # Remove trailing -

				response = urllib2.urlopen(url)
			except IOError:
				print("Failed to retrieve html for " + rider.name)
				return

			html = response.read()

			# Cache the html
			cacheDir   = self.getCacheDirectory()
			cachedFile = os.path.join(cacheDir, rider.cacheableName)
			f = open(cachedFile, "w")
			f.write(html)

		self._parseRiderHtml(rider, html)

	def trawl(self, rider):
		self._getRiderStats(rider)
