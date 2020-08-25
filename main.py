import pairing_generator as pg
import random
from commander import Commander

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

def convertStrToCommanderPair(inputStr):
	return tuple(map(Commander, inputStr.split("|")))

if __name__ == '__main__':
	pairings = getRemainingPairings()

	if(len(pairings) == 0):
		repopulatePairings()
		pairings = getRemainingPairings()

	pair = random.choice(pairings)

	pair = convertStrToCommanderPair(random.choice(pairings))

	

