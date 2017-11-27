class Player():
	def __init__(self,name,world):
		self.name = name
		self.world = world
	
	def __str__(self):
		return self.name + "\n" + self.world
	def __repr__(self):
		return self.name