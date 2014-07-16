from AbstractExporter import AbstractExporter

class EmberFixtureExporter(AbstractExporter):

	def _exportRiders(self, riders):
		text  = "App.Riders.FIXTURES = ["

		for i in range(0, len(riders)):
			rider = riders[i]

			text += "\n\t{ "
			text += "id: " + str(i) + ", "
			text += "name: \"" + rider.name + "\", "
			text += "age: " + str(rider.age) + ", "
			text += "weight: " + str(rider.weight) + ", "
			text += "height: " + str(rider.height)
			text += " },"

		text = text[:-1] # Remove last comma

		text += "\n];"

		return text

	def _exportMetrics(self, metrics):
		text = "App.Metrics.FIXTURES = ["

		text += "\n\t{ id: 0, "
		text += "averageAge: " + str(metrics.averageAge) + ", "
		text += "averageWeight: " + str(metrics.averageWeight) + ", "
		text += "averageHeight: " + str(metrics.averageHeight)
		text += "}"
		text += "\n];"

		return text

	def export(self, riders, metrics):
		fileContent = ""
		fileContent += self._exportRiders(riders)
		fileContent += "\n\n"
		fileContent += self._exportMetrics(metrics)

		f = open("data.js", "w")
		f.write(fileContent)
