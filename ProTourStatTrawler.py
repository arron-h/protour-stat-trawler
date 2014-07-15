import urllib2, sys, re, os

WIKIPEDIA_BASE_URL = "http://en.wikipedia.org"

weightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>")
weightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Weight</th>\n<td>([0-9\.]+)[&#160;]*\s?(kg|KG|Kg|kilograms).*?</td>", re.MULTILINE)

heightCheckRx = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>")
heightRx      = re.compile("<th scope=\"row\" style=\"text-align:left;\">Height</th>\n<td>([0-9\.]+)[&#160;]*\s?(M|m|cm|CM|Cm|metres).*?</td>", re.MULTILINE)

#	ageRx = re.compile("<th scope="row" style="tex-align:left;">Born</th><td><span style="display:none">(<span class="bday">1989-06-02</span>)</span> June 2, 1989 <span class="noprint ForceAgeToShow">(age&#160;25)</span><br /><a href="/wiki/Isernia" title="Isernia">Isernia</a>, <a href="/wiki/Italy" title="Italy">Italy</a></td>")

def buildSafeCacheFilename(str):
	return str.replace("/wiki/", "")

def buildRiderMap(riders):
	response = None
	try:
		response = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_2014_UCI_ProTeams_and_riders")
	except:
		print("Failed to grab url!")
		return

	html = response.read()

	prog = re.compile("<a href=\"(.*?)\"[^>]*>(.*?)</a>&#160;<span style=\"font-size:90%;\">\(<abbr title=\".*?\">[A-Z]{3}</abbr>\)</span></td>")
	matches = prog.findall(html)

	# Grab riders
	for match in matches:
		rider = {}
		rider["name"]   = match[1]
		rider["age"]    = None
		rider["height"] = None
		rider["weight"] = None
		rider["cache"]  = buildSafeCacheFilename(match[0])
		rider["url"]    = WIKIPEDIA_BASE_URL + match[0]

		riders[match[0]] = rider

def normalizeHeight(expr):
	m = re.search("([0-9]+)[&#160;]*\s?(cm|CM|Cm).*", expr.group(0))
	if m:
		heightInCm = float(m.group(1))
		heightInM  = heightInCm * 0.01
		return str(heightInM)

	return expr.group(1)

def parseRiderHtml(rider, html, errors):
	if weightCheckRx.search(html):
		m = weightRx.search(html)
		if m:
			rider["weight"] = m.group(1)
		else:
			print("Failed to retrieve weight. Error matching regular expression.")
			errors["weight"].append(rider["name"])

	if heightCheckRx.search(html):
		m = heightRx.search(html)
		if m:
			rider["height"] = normalizeHeight(m)
		else:
			print("Failed to retrieve height. Error matching regular expression.")
			errors["height"].append(rider["name"])

def cachedFilePath(rider):
	return "/tmp/pagecache/" + rider["cache"]

def tryLoadRiderFromCache(rider):
	cachedFile = cachedFilePath(rider)
	if os.path.exists(cachedFile):
		f    = open(cachedFile, "r")
		html = f.read()

		return html

	return None

def getRiderStats(rider, errors):
	html = tryLoadRiderFromCache(rider)

	if not html:
		response = None
		try:
			response = urllib2.urlopen(rider["url"])
		except:
			print("Failed to retrieve html for " + rider["name"])
			return

		html = response.read()

		# Cache the html
		cachedFile = cachedFilePath(rider)
		f = open(cachedFile, "w")
		f.write(html)

	parseRiderHtml(rider, html, errors)

def main():
	# Make a cache folder
	if not os.path.exists("/tmp/pagecache"):
		os.mkdir("/tmp/pagecache")

	riders = {}
	errors = {"height": [], "weight": []}
	buildRiderMap(riders)

	totalHeight = 0
	heightCount = 0
	totalWeight = 0
	weightCount = 0

	for k in riders:
		rider = riders[k]

		print("Getting stats for " + rider["name"] + "...")
		getRiderStats(rider, errors)

		#  Work out quick average
		if (rider["height"]):
			totalHeight += float(rider["height"])
			heightCount += 1
		if (rider["weight"]):
			totalWeight += float(rider["weight"])
			weightCount += 1

	avgWeight = totalWeight / weightCount
	avgHeight = totalHeight / heightCount

	print("Average weight: " + str(avgWeight) + "("+str(weightCount)+")")
	print("Average height: " + str(avgHeight) + "("+str(heightCount)+")")

	# Print errors
	if len(errors["height"]) > 0:
		print("Height parse errors:")
		print(errors["height"])

	if len(errors["weight"]) > 0:
		print("Weight parse errors:")
		print(errors["weight"])

if __name__ == "__main__":
	main()
