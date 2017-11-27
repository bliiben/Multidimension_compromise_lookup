class Hypothese():
	def __init__(self, players, chanceOfWinning):
		self.players = players
		self.chanceOfWinning = chanceOfWinning
		self.playersGain = {}
		for player in players:
			self.playersGain[player] = player.world * chanceOfWinning

	def getPlayerGain( self,player ):
		return self.playersGain[player]
		