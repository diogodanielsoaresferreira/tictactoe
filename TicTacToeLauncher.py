from Human import Human
from RandomBot import RandomBot
from TicTacToeGame import TicTacToeGame
from QLearning import QLearningAgent
from Minimax import Minimax


def take_turn(game, agent):
	if not game.play(*agent.get_next_action(game)):
		print("ERROR: Could not play!")
		exit(1)
	
	game.print_board()
	winner = game.who_won()
	if winner > 0:
		print(f'Player {winner} won!')
		return True
	elif winner < 0:
		print("It's a tie!")
		return True

	return False

if __name__ == "__main__":
	game = TicTacToeGame()
	agent2 = Minimax()
	agent1 = QLearningAgent()
	#agent1 = Human()
	#agent1 = RandomBot()

	done = False
	game.print_board()

	while not done:
		done = take_turn(game, agent1)
		if done:
			break

		done = take_turn(game, agent2)
