from AbstractExporter import AbstractExporter

class EmberFixtureExporter(AbstractExporter):

	def _exportRiders(self, riders):
		text  = "App.Rider.FIXTURES = ["

		for i in range(0, len(riders)):
			rider = riders[i]

			text += "\n\t{ "
			text += "id: " + str(i) + ", "
			text += "name: \"" + rider.name + "\", "
			text += "age: " + str(rider.age) + ", "
			text += "weight: " + str(rider.weight) + ", "
			text += "height: " + str(rider.height) + ", "
			text += "country: \"" + str(rider.country) + "\""
			text += " },"

		text = text[:-1] # Remove last comma

		text += "\n];"

		return text

	def _exportMetrics(self, metrics):
		text = "App.Metrics.FIXTURES = ["

		textualAge = ("{:.1f}"
			.format(metrics.averageAge))
		textualWeight = ("{:.2f}"
			.format(metrics.averageWeight))
		textualHeight = ("{:.2f}"
			.format(metrics.averageHeight))

		text += "\n\t{ id: 0, "
		text += "averageAge: " + textualAge + ", "
		text += "averageWeight: " + textualWeight + ", "
		text += "averageHeight: " + textualHeight + ", "
		text += "countryRep: \"" + metrics.countryRep + "\", "
		text += "countryRepCount: " + str(metrics.countryRepCount)
		text += " }"
		text += "\n];"

		return text

	def _exportCountries(self, countries):
		text = "App.Country.FIXTURES = ["

		for key in countries:
			value = countries[key]

			text += "\n\t{ "
			text += "id: \"" + key + "\", "
			text += "name: \"" + value + "\""
			text += " },"

		text = text[:-1] # Remove last comma

		text += "\n];"

		return text


	def export(self, riders, metrics, countries):
		fileContent = ""
		fileContent += self._exportRiders(riders)
		fileContent += "\n\n"
		fileContent += self._exportMetrics(metrics)
		fileContent += "\n\n"
		fileContent += self._exportCountries(countries)

		f = open("data.js", "w")
		f.write(fileContent)
