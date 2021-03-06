import os, re, urllib2, sys
from AbstractStatsTrawler import AbstractStatsTrawler
from Models import Rider
from trawlers.sites.Wikipedia import Wikipedia

weightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Weight</th>")
weightRx      = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Weight</th>\n<td>([0-9\.]+)\s?(kg|KG|Kg|kilograms).*?</td>", re.MULTILINE)

heightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Height</th>")
heightRx      = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Height</th>\n<td>([0-9\.]+)\s?(M|m|cm|CM|Cm|metres).*?</td>", re.MULTILINE)

ageCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Born</th>")
ageRx      = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Born</th>\n<td>.*?([0-9]{2})\)</span>", re.MULTILINE|re.DOTALL)

teamCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Current\steam</th>")
teamRx      = re.compile("<th scope=\"row\" style=\"text-align:left[;]{0,1}\">Current\steam</th>\n<td class=\"note\"><a[^>]*>(.*?)</a>", re.MULTILINE|re.DOTALL)

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

		if ageCheckRx.search(html):
			m = ageRx.search(html)
			if m:
				rider.age = m.group(1)
			else:
				raise StandardError("Failed to retrieve age. Error matching regular expression.")

		if teamCheckRx.search(html):
			m = teamRx.search(html)
			if m:
				rider.team = m.group(1)
			else:
				raise StandardError("Failed to retrieve team. Error matching regular expression.")

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

			# Replace special strings
			special = {
				'&nbsp;' : ' ', 
				'&#160;' : ' ', '&amp;' : '&', '&quot;' : '"',
				'&lt;'   : '<', '&gt;'  : '>'
			}

			for (k,v) in special.items():
				html = html.replace(k, v)

			# Cache the html
			cachedFile = self._cachedFilePath(rider)
			f = open(cachedFile, "w")
			f.write(html)

		self._parseRiderHtml(rider, html)

	def trawl(self, rider):
		self._getRiderStats(rider)
