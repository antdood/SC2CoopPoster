from yaml import safe_load

class Commander:
	def __init__(self, name, details = None):
		self.name = name

		# get details from config if not supplied
		if (details == None):
			with open("config.yml", "r") as file:
				details = safe_load(file)["commanders"][name]

		self.race = details["race"]
		self.sc2cooplink = details["sc2cooplink"]
		self.wikilink = details["wikilink"]

	def __repr__(self):
		return "Commander : " + self.name

	def __str__(self):
		return self.name