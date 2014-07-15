import Models
from trawlers.TrawlerFactory import TrawlerFactory

def main():
	trawlerFactory = TrawlerFactory()

	riderListTrawler = trawlerFactory.getTrawlerForRiderList()
	riders = riderListTrawler.trawlRiderList(2014)

	totalHeight = 0
	heightCount = 0
	totalWeight = 0
	weightCount = 0

	for k in riders:
		rider = riders[k]
		riderStatsTrawler = getTrawlerForRiderStats(rider)

		print("Getting stats for " + rider.name + "...")
		riderStatsTrawler.trawlRiderStats(rider)

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
