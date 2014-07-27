import os, re, urllib2, sys
from AbstractListTrawler import AbstractListTrawler
from Models import Rider
from trawlers.sites.Wikipedia import Wikipedia

riderNameRx = re.compile("<a href=\"(.*?)\"[^>]*>(.*?)</a>&#160;<span style=\"font-size:90%;\">\(<abbr title=\"(.*?)\">([A-Z]{3})</abbr>\)</span></td>")
teamNameRx  = re.compile("<span class=\"mw-headline\" id=\".*?\"><a href=\"/wiki/.*?\" title=\".*?\">(.*?)</a></span>")

class WikipediaListTrawler(AbstractListTrawler):

	def _getHtml(self, year):
		response  = None
		try:
			response = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_"+
				str(year)+"_UCI_ProTeams_and_riders")
		except:
			raise IOError("Failed to open the url to Wikipedia.")

		html = response.read()

		return html

	def _getNextTeam(self, html, offset):
		match = teamNameRx.search(html[offset:])
		if not match:
			return (None, None)

		teamDesc = {}
		teamDesc["name"]  = match.group(1)
		teamDesc["start"] = offset + match.start(0)
		teamDesc["end"]   = -1

		return (teamDesc, offset + match.end(1))

	def _getNextRider(self, html, offset, start, end):
		match = riderNameRx.search(html[offset + start:end])
		if not match:
			return (None, None)

		riderDesc = {}
		riderDesc["wikiurl"] = match.group(1)
		riderDesc["name"]    = match.group(2)
		riderDesc["countryName"] = match.group(3)
		riderDesc["countryId"]   = match.group(4)

		return (riderDesc, offset + match.end(0))

	def trawl(self, year):
		teams     = []
		riders    = []
		countries = {}

		html = self._getHtml(year)

		# Find the team names, and their offsets
		offset = 0
		while(True):
			teamDesc, offset = self._getNextTeam(html, offset)
			if not teamDesc:
				break		

			# Set the previous team's end position to the next team's start
			if len(teams) > 0:
				teams[-1]["end"] = teamDesc["start"]

			# Check to make sure the previously found team isn't the same as the next one
			if len(teams) > 0 and teams[-1]["name"] == teamDesc["name"]:
				break

			teams.append(teamDesc)

		# Now loop the teams and find the riders belonging
		for team in teams:
			# Loop riders in team
			offset = 0
			while(True):
				riderDesc, offset = self._getNextRider(html, offset, team["start"], team["end"])
				if not riderDesc:
					break

				rider = Rider(riderDesc["name"])

				wikiData = {}
				wikiData["cache"] = Wikipedia.buildSafeCacheFilename(riderDesc["wikiurl"])
				wikiData["url"]   = Wikipedia.baseUrl + riderDesc["wikiurl"]

				rider.setTrawlerData(wikiData)

				# Grab country name
				countryId   = riderDesc["countryId"]
				countryName = riderDesc["countryName"]
				if not countryId in countries:
					countries[countryId] = countryName

				rider.country = countryId
				rider.team    = team["name"]

				riders.append(rider)

		return (riders, countries)
