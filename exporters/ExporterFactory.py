from ExporterTypes import ExporterTypes
from EmberFixtureExporter import EmberFixtureExporter

class ExporterFactory:
	
	@staticmethod
	def getExporter(type):
		if type == ExporterTypes.EMBER_FIXTURE:
			return EmberFixtureExporter()