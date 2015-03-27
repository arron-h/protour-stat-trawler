from metrics.MetricsCalculator import MetricsCalculator
from trawlers.TrawlerFactory import TrawlerFactory
from trawlers.TrawlerTypes import TrawlerTypes
from exporters.ExporterFactory import ExporterFactory
from exporters.ExporterTypes import ExporterTypes
from Models import Metrics

def main():
	riderListTrawler = TrawlerFactory.getTrawler(TrawlerTypes.LIST)
	errors  = []
	riders, countries = riderListTrawler.trawl(2015)
	metrics = Metrics()
	metricsCalculator = MetricsCalculator()

	if len(riders) == 0:
		raise Exception("No riders found! Something probably went wrong whilst trawling Wikipedia.")

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

	# Perform post-calc
	metricsCalculator.performPostCalculations(metrics)

	# Print errors
	if len(errors):
		print("Errors while trawling:-")
		for e in errors:
			print("\t" + e)

	# Export
	exporter = ExporterFactory.getExporter(ExporterTypes.EMBER_FIXTURE)
	exporter.export(riders, metrics, countries)

if __name__ == "__main__":
	main()
