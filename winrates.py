import re
from urllib.request import urlopen

# No endpoint to query for these stats, so let's do some messy scraping

html = ""
data = {}

def getRelevantHtml():
	global html

	if(html):
		return html

	url = "https://starcraft2coop.com/resources/stats"

	page = urlopen(url).read().decode("utf-8")

	i = page.index("var ctx = $('#communityCommanderWinRateChart');")

	html = page[i:i+750]

	return html


def getWinrateData():
	global data

	if(data):
		return data

	commanders = re.search("labels: \[(.+?)\]", getRelevantHtml()).group(1).replace("\"", "").split(",")

	wins, losses = map(lambda x: x.split(","), re.findall("data: \[(.+?)\]", getRelevantHtml()))

	wins = list(map(int, wins))
	losses = list(map(int, losses))

	for n, commander in enumerate(commanders):
		if(commander == "Horner"): # Hope no more exceptions come later on :/
			commander = "Han & Horner"
		data[commander] = {"wins" : wins[n], "losses" : losses[n]}

	return data


def getWinRateOf(commander):
	return getWinrateData()[commander]["wins"]/getTotalGameCount(commander) * 100

def getPickRateOf(commander):
	return getTotalGameCount(commander)/getTotalGameCount() * 100

def getTotalGameCount(commander = None):
	if(commander):
		return getWinrateData()[commander]["wins"]+getWinrateData()[commander]["losses"]
	else:
		total = 0

		for c in getWinrateData().values():
			total += c["wins"]
			total += c["losses"]

		return total