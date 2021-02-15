from Agent import Agent

class Human(Agent):
	def __init__(self):
		pass

	def get_next_action(self, board):
		return int(input()), int(input())
