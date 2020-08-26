from yaml import safe_load
from itertools import product, combinations
from commander import Commander
from file_handler import getFile

commanders = []

def getAllCommanders():
	global commanders
	if(commanders):
		return commanders

	with getFile("config.yml") as file:
		for commander, details in safe_load(file)["commanders"].items():
			commanders.append(Commander(commander, details))
			
	return commanders

def getCompletePairings():
	return list(combinations(getAllCommanders(),2))

def getNewCommanderPairings(commanderName = ""):
	# if no commanderName was supplied, commander with latest release date is assumed to be the new commander
	if(not commanderName):
		newCommander = max(getAllCommanders(), key = lambda x: x.date)
	else:
		for commander in getAllCommanders():
			if commander.name == commanderName:
				newCommander = commander
				break

	oldCommanderList = filter(lambda com: com != newCommander, getAllCommanders())

	return list(product([newCommander], oldCommanderList))
