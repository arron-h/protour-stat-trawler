class AbstractExporter:

	def export(self, riders, metrics, countries):
		raise NotImplementedError("AbstractExporter: export() not implemented!")