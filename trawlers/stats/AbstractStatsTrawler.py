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

	def getName(self):
		raise NotImplementedError("AbstractTrawler: getName() not implemented!")

