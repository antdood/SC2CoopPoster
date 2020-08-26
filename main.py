import pairing_generator as pg
import random
import datetime
from commander import Commander
from yaml import safe_load, dump
from reddit_thingamabobs import getRedditInstance, getSubredditInstance, getRedditLink
from more_itertools import take
from file_handler import getFile

def getRemainingPairings():
	with getFile("remaining_pairings.txt") as file:
		# readlines() includes the \n :facepalm:
		#return file.readlines()
		return file.read().splitlines()

def repopulatePairings():
	with getFile("remaining_pairings.txt", "w") as file:
		for pair in pg.getCompletePairings():
			file.write(str(pair[0]) + "|" + str(pair[1]) + "\n")

	return

def removePairingFromFile(pair):
	lines = []
	with getFile("remaining_pairings.txt", "r") as file:
		lines = file.read().splitlines()

	lines.remove(pair)

	with getFile("remaining_pairings.txt", "w") as file:
		for line in lines:
			file.write(line + "\n")

	return

def convertStrToCommanderPair(inputStr):
	return tuple(map(Commander, inputStr.split("|")))

def getCurrentPostNumber():
	return len(getPostHistory()) + 1

def getPostHistory():
	with getFile("config.yml", "r") as file:
		return safe_load(file)["posthistory"] or {}

def generatePostHistoryEntry(postID, pair):
	return {"url" : getRedditLink(postID).url, "pair" : pair}

def addPostHistory(entry):
	with getFile("config.yml", "r") as file:
		config = safe_load(file)

	# for first run, should be a better way to do this 
	if(config["posthistory"] == None):
		config["posthistory"] = {}

	config["posthistory"][getCurrentPostNumber()] = entry

	with getFile("config.yml", "w") as file:
		dump(config, file)

	return

def generatePrevPostSection():
	postHistory = getPostHistory()

	if(postHistory == {}):
		return ""
	else:
		with getFile("Reddit Post Templates/previousPostSectionTemplate.md") as prevPostSectionFile, \
			 getFile("Reddit Post Templates/previousPostTemplate.md") as prevPostFile:

			prevPostSectTemplate = prevPostSectionFile.read()
			prevPostTemplate = prevPostFile.read()

			prevPostSectText = ""
			for postNumber, details in take(5, reversed(postHistory.items())):
				prevPostSectText += prevPostTemplate.format(postNumber, **details) + "\n"

			return prevPostSectTemplate.format(prevPostSectText)

if(__name__ == '__main__'):
	today = datetime.date.today()
	if(today.weekday() == 2):
		pairings = getRemainingPairings()

		if(len(pairings) == 0):
			repopulatePairings()
			pairings = getRemainingPairings()

		pair = random.choice(pairings)
		commander_pair = convertStrToCommanderPair(pair)

		with getFile("Reddit Post Templates/mainTemplate.md") as mainFile, \
			 getFile("Reddit Post Templates/commanderTemplate.md") as commanderFile, \
			 getFile("Reddit Post Templates/titleTemplate.md") as titleFile:

			mainTemplate = mainFile.read()
			commanderTemplate = commanderFile.read()
			titleTemplate = titleFile.read()

		prevPostSect = generatePrevPostSection()

		title = titleTemplate.format(postnumber = getCurrentPostNumber(), commander1 = commander_pair[0].name, commander2 = commander_pair[1].name)
		text = mainTemplate.format(commander1 = commanderTemplate.format(commander_pair[0]), commander2 = commanderTemplate.format(commander_pair[1]), prevPostSect = prevPostSect)

		postID = getSubredditInstance().submit(title, selftext = text)
		
		addPostHistory(generatePostHistoryEntry(postID, pair))
		removePairingFromFile(pair)
