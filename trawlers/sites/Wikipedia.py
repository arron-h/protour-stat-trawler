class Wikipedia:
	
	@staticmethod
	def buildSafeCacheFilename(url):
		return url.replace("/wiki/", "")

	baseUrl = "http://en.wikipedia.org"