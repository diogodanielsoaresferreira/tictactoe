import random

from Agent import Agent

class RandomBot(Agent):
	def __init__(self):
		pass

	def get_next_action(self, board):
		possible_actions = board.get_available_positions()
		return random.choice(possible_actions)
