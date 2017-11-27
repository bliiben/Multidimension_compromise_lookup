import numpy as np
from math import sin,pi
from Player import Player
import itertools
import operator
from Hypothese import Hypothese
from Option import Option

class Game():
	PRECISION = 100
	def __init__(self, file):
		self.players = self.generatePlayers(file)

	def play( self ):
		hypotheses = self.generateOptions()
		result = self.playOptions(hypotheses)
		for option in result :
			print option
			for p in option.getPlayers() : 
				print "--> " , option.getPlayerGain(p)
				
	def playOptions(self, hypotheses ):
		options=[]
		for hypothese in hypotheses:
			#chanceOfWinning is just used to get the id
			print "Warning fixed value here"
			for oIndex in range(10000):
				options.append( Option(hypothese, oIndex) )

		playersOptions={}
		for player in self.players:
			playersOptions[player] = []
			for option in options:
				if( player in option.getPlayers() ):
					playersOptions[player].append(option)
			playersOptions[player] = sorted(playersOptions[player],key=lambda o: o.getPlayerGain(player) , reverse = True)
		return self.finalizeOption(playersOptions)

	def finalizeOption(self, playersOptions ):

		playersLeft = self.players
		removedPlayer = []
		n = 0
		optionsLeft = True
		choosenOptions = []
		while len(playersLeft) != 0:
			for player in playersLeft:
				allPlayerIn = True
				
				for requiredPlayer in playersOptions[player][n].getPlayers() :
					if( requiredPlayer in removedPlayer ):
						allPlayerIn = False
					allPlayerIn = allPlayerIn and (playersOptions[player][n] in playersOptions[requiredPlayer][0:n+1])

				if( allPlayerIn ):
					#print ("Option : ", str(playersOptions[player][n])," has been accepted")
					choosenOptions.append( playersOptions[player][n] )
					for p in playersOptions[player][n].getPlayers():
						playersLeft.remove(p)
						removedPlayer.append(p)
			
			n+=1
		
		return choosenOptions
	def generateOptions( self ):
		hypotheses = []
		playersTruthTable = list(itertools.product([False, True], repeat=len(self.players)))
		for playersTruthLine in playersTruthTable:
			players=[]
			for playerIndex in range(len(self.players)):
				if( playersTruthLine[playerIndex] ):
					players.append(self.players[playerIndex])

			#Making hypotheses to assemble players
			if( len(players) ):
				# Our players
				worldSum=np.zeros(self.shape)
				for player in players:
					worldSum = player.world + worldSum
					
				# Get the other player total
				otherTotal=0
				for otherPlayer in [ otherPlayer for otherPlayer in self.players if otherPlayer not in players ]:
					otherTotal += np.max(otherPlayer.world)

				#Getting the chances of winning for players
				chanceOfWinning = worldSum / ( otherTotal + worldSum )
				chanceOfWinning = np.nan_to_num(chanceOfWinning)

				hypotheses.append(Hypothese(players, chanceOfWinning))
		return hypotheses
	def makeOptions(self, dimensions, players ):
		print dimensions, players
	def generatePlayers(self, file ):
		with open(file) as f:
			lines = f.read().replace("	","").split("\n")

		## Extracting the information from the file
		# table separated by |
		# position of the player on the subject separated by ; as position;influence;clout

		self.dimensions = lines[0].split("|")[1:]
		players = []
		for stringLine in lines[1:]:
			l = stringLine.split("|")
			name = l[0]
			player = { "name" : name }
			for dI in range(len(self.dimensions)):
				parameters = map(float,l[dI+1].split(";"))
				player[self.dimensions[dI]] = Game.powerFunction(parameters[0],parameters[1],parameters[2])
			players.append(player)

		## Generate the multidimensional space for every player
		playersObjects=[]
		for player in players :
			total = np.array(0)
			for dimension in self.dimensions:
				total = np.add.outer(total,player[dimension])
			playersObjects.append(Player(player["name"], total))

		self.shape = playersObjects[0].world.shape
		
		return playersObjects

	@staticmethod
	def powerFunction( position, influence, clout ):
		position = position
		clout = clout
		graph = [0] * Game.PRECISION
		start = position - ( clout / 2)
		end = position + ( clout / 2)

		if( position >= end or position <= start):
			return graph
		for x in range( 0,Game.PRECISION):
			graph[x] = min(sin( ( min( position , max( start , x) ) - ( start ) )*pi / ( position-start ) / 2 ) * (influence) , sin( ( min( position + (end-position), max( position , x) )-( position - (end-position)) )* pi / (end-position) /2) *(influence) )
		return np.array(graph)
		