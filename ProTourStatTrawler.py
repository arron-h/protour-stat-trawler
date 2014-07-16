import Models
from trawlers.TrawlerFactory import TrawlerFactory
from trawlers.TrawlerTypes import TrawlerTypes

def main():
	riderListTrawler = TrawlerFactory.getTrawler(TrawlerTypes.LIST)
	riders = riderListTrawler.trawl(2014)
	errors = []

	totalHeight = 0
	heightCount = 0
	totalWeight = 0
	weightCount = 0

	for rider in riders:
		riderStatsTrawler = TrawlerFactory.getTrawler(TrawlerTypes.STATS)

		print("Getting stats for " + rider.name + "...")
		try:
			riderStatsTrawler.trawl(rider)
		except StandardError, e:
			errors.append(rider.name + ": " + str(e))
			print("Failed: " + str(e))
			continue

		#  Work out quick average
		if (rider.height):
			totalHeight += float(rider.height)
			heightCount += 1
		if (rider.weight):
			totalWeight += float(rider.weight)
			weightCount += 1

	avgWeight = totalWeight / weightCount
	avgHeight = totalHeight / heightCount

	print("Average weight: " + str(avgWeight) + "("+str(weightCount)+")")
	print("Average height: " + str(avgHeight) + "("+str(heightCount)+")")

if __name__ == "__main__":
	main()
