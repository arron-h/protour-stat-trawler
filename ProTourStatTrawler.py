from metrics.MetricsCalculator import MetricsCalculator
from trawlers.TrawlerFactory import TrawlerFactory
from trawlers.TrawlerTypes import TrawlerTypes
from exporters.ExporterFactory import ExporterFactory
from exporters.ExporterTypes import ExporterTypes
from Models import Metrics

def main():
	riderListTrawler = TrawlerFactory.getTrawler(TrawlerTypes.LIST)
	errors  = []
	riders  = riderListTrawler.trawl(2014)
	metrics = Metrics()
	metricsCalculator = MetricsCalculator()
	
	# Trawl
	for rider in riders:
		riderStatsTrawler = TrawlerFactory.getTrawler(TrawlerTypes.STATS)

		print("Getting stats for " + rider.name + "...")
		try:
			riderStatsTrawler.trawl(rider)
		except StandardError, e:
			errors.append(rider.name + ": " + str(e))
			continue

		metricsCalculator.recalculate(metrics, rider)

	# Export
	exporter = ExporterFactory.getExporter(ExporterTypes.EMBER_FIXTURE)
	exporter.export(riders, metrics)

if __name__ == "__main__":
	main()
