import pairing_generator as pg
import random
from commander import Commander
from yaml import safe_load, dump
from reddit_thingamabobs import getRedditInstance

def getRemainingPairings():
	with open("remaining_pairings.txt", "r") as file:
		# readlines() includes the \n :facepalm:
		#return file.readlines()
		return file.read().splitlines()

def repopulatePairings():
	with open("remaining_pairings.txt", "w") as file:
		for pair in pg.getCompletePairings():
			file.write(str(pair[0]) + "|" + str(pair[1]) + "\n")

	return

def removePairingFromFile(pair):
	lines = []
	with open("remaining_pairings.txt", "r") as file:
		lines = file.read().splitlines()

	lines.remove(pair)

	with open("remaining_pairings.txt", "w") as file:
		for line in lines:
			file.write(line + "\n")

	return

def getPostNumber():
	with open("config.yml", "r") as file:
		return safe_load(file)["postnumber"]

def increasePostNumber():
	with open("config.yml", "r") as file:
		config = safe_load(file)
		config["postnumber"] += 1

	with open("config.yml", "w") as file:
		dump(config, file)

def convertStrToCommanderPair(inputStr):
	return tuple(map(Commander, inputStr.split("|")))

if(__name__ == '__main__'):
	pairings = getRemainingPairings()

	if(len(pairings) == 0):
		repopulatePairings()
		pairings = getRemainingPairings()

	pair = random.choice(pairings)
	commander_pair = convertStrToCommanderPair(pair)

	with open("Reddit Post Templates/mainTemplate.md") as mainFile, \
		 open("Reddit Post Templates/commanderTemplate.md") as commanderFile, \
		 open("Reddit Post Templates/titleTemplate.md") as titleFile:

		mainTemplate = mainFile.read()
		commanderTemplate = commanderFile.read()
		titleTemplate = titleFile.read()

	title = titleTemplate.format(postnumber = getPostNumber(), commander1 = commander_pair[0].name, commander2 = commander_pair[1].name)
	text = mainTemplate.format(commander1 = commanderTemplate.format(commander_pair[0]), commander2 = commanderTemplate.format(commander_pair[1]))

	getRedditInstance().submit(title, selftext = text)

	increasePostNumber()
	removePairingFromFile(pair)