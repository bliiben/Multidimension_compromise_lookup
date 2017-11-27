import numpy as np
class Option():
	def __init__(self, hypothese, index):
		self.hypothese = hypothese
		self.index = index

	def getPlayers(self):
		return self.hypothese.players

	def getPlayerGain(self, player):
		return np.take(self.hypothese.getPlayerGain(player),self.index)

	def __str__(self):
		return "Option : " + ", ".join(map(lambda x:x.name, self.getPlayers())) + " on " + str(self.index)