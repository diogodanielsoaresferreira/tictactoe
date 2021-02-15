import pickle
import random
import operator
import numpy as np

from Agent import Agent
from RandomBot import RandomBot
from TicTacToeGame import TicTacToeGame


class QLearningAgent(Agent):
	
	def __init__(self):

		self.epochs = 2500
		self.Q_table = {}

		self.epsilon = 0.3
		self.learning_rate = 0.2
		self.gamma = 0.9

		self.winning_reward = 10
		self.losing_reward = -10
		self.tie_reward = -5
		self.step_reward = -1

		self.Q_table_filepath = "qtable.p"
		self.opponent_agent_training = RandomBot()

		try:
			with open(self.Q_table_filepath, 'rb') as f:
				self.Q_table = pickle.load(f)
		except:
			print(f'Could not load Q-table from {self.Q_table_filepath}. Initializing empty Q-Table.')

	def train(self):
		for epoch in range(self.epochs):
			game = TicTacToeGame()
			game_done = False

			while not game_done:

				state = self._hash_board(game.board)
				if state not in self.Q_table:
					self.Q_table[state] = {action: 0}

				action = self._epsilon_greedy_policy(game)
				if action not in self.Q_table[state]:
					self.Q_table[state][action] = 0

				self._make_move(game, action)
				reward, game_done = self._calculate_reward(game)	
				if game_done:
					self._update_qtable(game.board, state, action, reward)
					break

				self._opponent_move(game)
				self._update_qtable(game.board, state, action, reward)

		with open(self.Q_table_filepath, 'wb') as f:
			pickle.dump(self.Q_table, f)

	def get_next_action(self, game):
		return self._greedy_policy(game)

	def _update_qtable(self, board, state, action, reward):
		new_state = self._hash_board(board)
		if new_state not in self.Q_table:
			self.Q_table[new_state] = {action: 0}
		
		self.Q_table[state][action] = self.Q_table[state][action] + \
						self.learning_rate * (reward + self.gamma * max(self.Q_table[new_state].values()) - self.Q_table[state][action])

	def _make_move(self, game, action):
		if not game.play(*action):
			print("ERROR: Could not play!")
			exit(1)

	def _hash_board(self, board):
		return str(board.reshape(board.shape[0] * board.shape[1]))

	def _epsilon_greedy_policy(self, game):
		if(random.uniform(0,1) > self.epsilon):
			return self._greedy_policy(game)
		
		return random.choice(game.get_available_positions())

	def _greedy_policy(self, game):
		state = self._hash_board(game.board)
		possible_actions = game.get_available_positions()
		possible_actions_with_score = {action:self.Q_table.get(state)[action] for action in self.Q_table.get(state, {}) if action in possible_actions}
		if len(possible_actions_with_score) == 0:
			return random.choice(possible_actions)
		return max(possible_actions_with_score.items(), key=operator.itemgetter(1))[0]

	def _opponent_move(self, game):
		opponent_action = self.opponent_agent_training.get_next_action(game)
		self._make_move(game, opponent_action)


	def _calculate_reward(self, game):
		winner = game.who_won()
		if winner == 1:
			return self.winning_reward, True
		elif winner == -1:
			return self.tie_reward, True
		elif winner == 2:
			return self.losing_reward, True

		return self.step_reward, False


if __name__ == "__main__":
	agent = QLearningAgent()
	agent.train()
