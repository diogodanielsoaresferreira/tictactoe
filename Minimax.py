import operator

from copy import deepcopy
from Agent import Agent

class Minimax(Agent):
	def __init__(self):

		self.turn = 2
		self.winning_reward = 10
		self.losing_reward = -10
		self.tie_reward = 0

	def get_next_action(self, board):
		available_positions = board.get_available_positions()
		possible_rewards = {position: self._minimax(deepcopy(board), position) for position in available_positions}
		return max(possible_rewards.items(), key=operator.itemgetter(1))[0]

	def _minimax(self, game, action, depth=0):
		game.play(*action)
		reward, done = self._calculate_reward(game)
		if not done:
			available_positions = game.get_available_positions()
			possible_rewards = [self._minimax(deepcopy(game), position, depth+1) for position in available_positions]
			return min(possible_rewards) if depth%2 == 0 else max(possible_rewards)
		return reward


	def _calculate_reward(self, game):
		winner = game.who_won()
		if winner == self.turn:
			return self.winning_reward, True
		elif winner == -1:
			return self.tie_reward, True
		elif winner == 0:
			return 0, False
		
		return self.losing_reward, True
