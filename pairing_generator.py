import yaml

commanders = {}

def getCommanders():
	global commanders
	if(commanders):
		return commanders

	myFile = open("config.yml", "r")

	myYaml = yaml.safe_load(myFile)

	myFile.close()
	print("hi")

	commanders = myYaml['commanders']

	return commanders


print(getCommanders())

print(getCommanders())

