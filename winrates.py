import re
from urllib.request import urlopen

winrates = {}

def getWinRateOf(commanderName):
	return getPickAndWinRateOf(commanderName)[1] * 100

def getPickRateOf(commanderName):
	return getPickAndWinRateOf(commanderName)[0] * 100

def getPickAndWinRateOf(commanderName):
	if(commanderName == "Han & Horner"): # Hope no more exceptions come later on :/
		commanderName = "Horner"

	if(commanderName in winrates.keys()):
		return winrates[commanderName]

	url = "https://starcraft2coop.com/scripts/endpoints/reddit.php?commander=" + commanderName

	# url returns '[<pickrate>, <winrate>]'
	winrates[commanderName] = tuple(eval(urlopen(url).read()))
	return winrates[commanderName]