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

	def export(self, riders, metrics):
		fileContent = ""
		fileContent += self._exportRiders(riders)

		f = open("data.js", "w")
		f.write(fileContent)
