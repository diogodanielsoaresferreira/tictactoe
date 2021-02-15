import numpy as np

ROW_SIZE = 3
COLUMN_SIZE = 3

PLAYER_1_ID = 1
PLAYER_2_ID = 2
PLAYER_1_MARK = 'O'
PLAYER_2_MARK = 'X'
CONSECUTIVE_MARKS_TO_WIN = 3

class TicTacToeGame:

	def __init__(self):
		self.turn = 0
		self.rows = ROW_SIZE
		self.columns = COLUMN_SIZE
		self.board = np.zeros((ROW_SIZE, COLUMN_SIZE), dtype=np.int)

	def get_available_positions(self):
		avail_positions = []
		for x in range(self.rows):
			for y in range(self.columns):
				if self.board[x,y] == 0:
					avail_positions.append((x,y))
		return avail_positions

	def play(self, x, y):
		if x<0 or x>=self.rows or y<0 or y>=self.columns or self.board[x, y] != 0:
			return False

		player_mark = PLAYER_1_ID if self.turn%2==0 else PLAYER_2_ID
		self.board[x, y] = player_mark
		self.turn += 1
		return True

	def who_won(self):
		who_hor = self._who_won_horizontally()
		if who_hor != 0:
			return who_hor

		who_ver = self._who_won_vertically()
		if who_ver != 0:
			return who_ver

		who_diag = self._who_won_diagonally()
		if who_diag != 0:
			return who_diag

		if len(self.get_available_positions()) == 0:
			return -1

		return 0

	def print_board(self):
		print('  ', end="")
		for column in range(self.columns):
			print(f'  {column}', end=" ")
		print()

		for row in range(self.rows):
			print(f'{row} ', end="")
			for column in range(self.columns):
				print(f'| {self._print_player_mark(self.board[row, column])}', end=" ")
			print("|")

	def _print_player_mark(self, mark):
		if mark == PLAYER_1_ID:
			return PLAYER_1_MARK
		elif mark == PLAYER_2_ID:
			return PLAYER_2_MARK
		return ' '

	def _who_won_horizontally(self):
		current_mark = 0
		consecutive_mark = 0
		for x in range(self.rows):
			for y in range(self.columns):
				if current_mark != self.board[x, y]:
					current_mark = self.board[x, y]
					consecutive_mark = 1
				else:
					consecutive_mark += 1
				if current_mark != 0 and consecutive_mark == CONSECUTIVE_MARKS_TO_WIN:
					return current_mark

			current_mark = 0
			consecutive_mark = 0
		return 0

	def _who_won_vertically(self):
		current_mark = 0
		consecutive_mark = 0
		for y in range(self.columns):
			for x in range(self.rows):
				if current_mark != self.board[x, y]:
					current_mark = self.board[x, y]
					consecutive_mark = 1
				else:
					consecutive_mark += 1
				if current_mark != 0 and consecutive_mark == CONSECUTIVE_MARKS_TO_WIN:
					return current_mark

			current_mark = 0
			consecutive_mark = 0
		return 0

	def _who_won_diagonally(self):
		for x in range(self.rows):
			for y in range(self.columns):
				if self.board[x, y] != 0:
					who_won = self._check_diagonal_down_recursive(x, y)
					if who_won != 0:
						return who_won
					who_won = self._check_diagonal_up_recursive(x, y)
					if who_won != 0:
						return who_won
		return 0

	def _check_diagonal_down_recursive(self, x, y, number_hits=1):
		if number_hits == CONSECUTIVE_MARKS_TO_WIN:
			return self.board[x, y]

		if x+1 >= self.rows or y-1 < 0 or self.board[x+1, y-1] != self.board[x, y]:
			return 0

		return self._check_diagonal_down_recursive(x+1, y-1, number_hits+1)

	def _check_diagonal_up_recursive(self, x, y, number_hits=1):
		if number_hits == CONSECUTIVE_MARKS_TO_WIN:
			return self.board[x, y]

		if x+1 >= self.rows or y+1 >= self.columns or self.board[x+1, y+1] != self.board[x, y]:
			return 0

		return self._check_diagonal_up_recursive(x+1, y+1, number_hits+1)

if __name__ == "__main__":
	game = TicTacToeGame()
	game.print_board()
	while True:
		print(game.play(int(input()), int(input())))
		game.print_board()
		if game.who_won() != 0:
			print(f'Player {game.who_won()} won!')
			break
