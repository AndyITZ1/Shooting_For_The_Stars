from abc import ABC, abstractmethod


# Abstract game screen class with update and draw function.
# Menu screens and the main gameplay screen should inherit from this class.
class GameScreen(ABC):
	def __init__(self, game):
		self.game = game
	
	@abstractmethod
	def update(self):
		pass
	
	@abstractmethod
	def render(self):
		pass
