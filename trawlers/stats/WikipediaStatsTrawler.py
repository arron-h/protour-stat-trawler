import os, re, urllib2, sys
from AbstractStatsTrawler import AbstractStatsTrawler
from Models import Rider
from trawlers.sites.Wikipedia import Wikipedia

weightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>")
weightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>\n<td>([0-9\.]+)[&#160;]*\s?(kg|KG|Kg|kilograms).*?</td>", re.MULTILINE)

heightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>")
heightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>\n<td>([0-9\.]+)[&#160;]*\s?(M|m|cm|CM|Cm|metres).*?</td>", re.MULTILINE)

class WikipediaStatsTrawler(AbstractStatsTrawler):

	def __init__(self):
		if not os.path.exists("/tmp/pagecache"):
			os.mkdir("/tmp/pagecache")

	def _normalizeHeight(self, expr):
		m = re.search("([0-9]+)[&#160;]*\s?(cm|CM|Cm).*", expr.group(0))
		if m:
			heightInCm = float(m.group(1))
			heightInM  = heightInCm * 0.01
			return str(heightInM)

		return expr.group(1)

	def _parseRiderHtml(self, rider, html):
		if weightCheckRx.search(html):
			m = weightRx.search(html)
			if m:
				rider.weight = m.group(1)
			else:
				raise StandardError("Failed to retrieve weight. Error matching regular expression.")

		if heightCheckRx.search(html):
			m = heightRx.search(html)
			if m:
				rider.height = self._normalizeHeight(m)
			else:
				raise StandardError("Failed to retrieve height. Error matching regular expression.")

	def _cachedFilePath(self, rider):
		return "/tmp/pagecache/" + rider.implData["cache"]

	def _tryLoadRiderFromCache(self, rider):
		cachedFile = self._cachedFilePath(rider)
		if os.path.exists(cachedFile):
			f    = open(cachedFile, "r")
			html = f.read()

			return html

		return None

	def _getRiderStats(self, rider):
		html = self._tryLoadRiderFromCache(rider)

		if not html:
			response = None
			try:
				response = urllib2.urlopen(rider.implData["url"])
			except:
				print("Failed to retrieve html for " + rider.name)
				return

			html = response.read()

			# Cache the html
			cachedFile = self._cachedFilePath(rider)
			f = open(cachedFile, "w")
			f.write(html)

		self._parseRiderHtml(rider, html)

	def trawl(self, rider):
		self._getRiderStats(rider)
