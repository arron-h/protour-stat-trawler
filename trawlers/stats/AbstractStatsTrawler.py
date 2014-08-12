import tempfile, os

class AbstractStatsTrawler:

	def __init__(self):
		cacheDir = self.getCacheDirectory()
		if not os.path.exists(cacheDir):
			os.makedirs(cacheDir)

	def trawl(self, rider):
		raise NotImplementedError("AbstractTrawler: trawl() not implemented!")

	def getCacheDirectory(self):
		return os.path.join(
			tempfile.gettempdir(),
			"protrawler",
			self.getName())

	def _tryLoadRiderFromCache(self, rider):
		cacheDir   = self.getCacheDirectory()
		cachedFile = os.path.join(cacheDir, rider.cacheableName)
		if os.path.exists(cachedFile):
			f    = open(cachedFile, "r")
			html = f.read()

			return html

		return None

	def getName(self):
		raise NotImplementedError("AbstractTrawler: getName() not implemented!")

