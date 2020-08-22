class Commander:
	def __init__(self, name, details):
		self.name = name
		self.race = details["race"]
		self.sc2cooplink = details["sc2cooplink"]
		self.wikilink = details["wikilink"]
