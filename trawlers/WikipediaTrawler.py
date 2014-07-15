import os, re, urllib2, sys
from AbstractTrawler import AbstractTrawler
import Models


WIKIPEDIA_BASE_URL = "http://en.wikipedia.org"

weightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>")
weightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>\n<td>([0-9\.]+)[&#160;]*\s?(kg|KG|Kg|kilograms).*?</td>", re.MULTILINE)

heightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>")
heightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>\n<td>([0-9\.]+)[&#160;]*\s?(M|m|cm|CM|Cm|metres).*?</td>", re.MULTILINE)

class WikipediaTrawler(AbstractTrawler):

	def __init__(self):
		if not os.path.exists("/tmp/pagecache"):
			os.mkdir("/tmp/pagecache")

	def _buildSafeCacheFilename(str):
		return str.replace("/wiki/", "")

	def _buildRiderList(year):
		response = None
		riders   = []

		try:
			response = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_2014_UCI_ProTeams_and_riders")
		except:
			raise IOError("Failed to open the url to Wikipedia.")

		html = response.read()

		prog    = re.compile("<a href=\"(.*?)\"[^>]*>(.*?)</a>&#160;<span style=\"font-size:90%;\">\(<abbr title=\".*?\">[A-Z]{3}</abbr>\)</span></td>")
		matches = prog.findall(html)

		# Grab riders
		for match in matches:
			rider = Rider(match[1])

			wikiData = {}
			wikiData["cache"] = _buildSafeCacheFilename(match[0])
			wikiData["url"]   = WIKIPEDIA_BASE_URL + match[0]

			rider.setTrawlerData(wikiData)

			riders.append(rider)

		return riders

	def _normalizeHeight(expr):
		m = re.search("([0-9]+)[&#160;]*\s?(cm|CM|Cm).*", expr.group(0))
		if m:
			heightInCm = float(m.group(1))
			heightInM  = heightInCm * 0.01
			return str(heightInM)

		return expr.group(1)

	def _parseRiderHtml(rider, html):
		if weightCheckRx.search(html):
			m = weightRx.search(html)
			if m:
				rider["weight"] = m.group(1)
			else:
				raise StandardError("Failed to retrieve weight. Error matching regular expression.")

		if heightCheckRx.search(html):
			m = heightRx.search(html)
			if m:
				rider["height"] = _normalizeHeight(m)
			else:
				raise StandardError("Failed to retrieve height. Error matching regular expression.")

	def _cachedFilePath(rider):
		return "/tmp/pagecache/" + rider.trawlerData["cache"]

	def _tryLoadRiderFromCache(rider):
		cachedFile = _cachedFilePath(rider)
		if os.path.exists(cachedFile):
			f    = open(cachedFile, "r")
			html = f.read()

			return html

		return None

	def _getRiderStats(rider):
		html = _tryLoadRiderFromCache(rider)

		if not html:
			response = None
			try:
				response = urllib2.urlopen(rider.trawlerData["url"])
			except:
				print("Failed to retrieve html for " + rider["name"])
				return

			html = response.read()

			# Cache the html
			cachedFile = cachedFilePath(rider)
			f = open(cachedFile, "w")
			f.write(html)

		parseRiderHtml(rider, html, errors)

	def trawlRiderStats(self, rider):
		_getRiderStats(rider)

	def trawlRiderList(self, year):
		return self._buildRiderList(year)