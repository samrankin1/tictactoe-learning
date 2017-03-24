import random

from enum import Enum

from database import DatabaseManager
import stats

VALID_COLUMNS		 = ('a', 'b', 'c')
VALID_ROWS			 = ('1', '2', '3')
VALID_TILE_STATES	 = ('b', 'i', 'o') # b = blank, i = controlled by player (X/O), o = controlled by opponent (X/O)

DEFAULT_TILE_STATE	 = 'b'

SPECIAL_WIN_CASES = [[('a', '1'), ('b', '2'), ('c', '3')], [('a', '3'), ('b', '2'), ('c', '1')]] # hard-coded diagonal win-cases # TODO: define these more elegantly

class Result(Enum):
	WIN = 0
	LOSS = 1
	DRAW = 2

class Board:

	def __init__(self, initial_state = None):
		if initial_state is None:
			self.board_state = {}
		else:
			self.board_state = initial_state # TODO: verify

		self.move_history = []

	@staticmethod
	def from_board_string(board_string):
		tile_states = [board_string[i:(i + 3)] for i in range(0, len(board_string), 3)] # separate into groups of three chars e.g.: ["a2i", "b2o", "b3o"]
		initial_state = {}
		for tile_state in tile_states: # reconstruct the board_state dict
			assert (tile_state[0] in VALID_COLUMNS)
			assert (tile_state[1] in VALID_ROWS)
			assert (tile_state[2] in VALID_TILE_STATES)

			initial_state[tile_state[:2]] = tile_state[2] # e.g.: {"a2": "i", "b2": "o", "b3": "o"}

		return Board(initial_state = initial_state)

	def to_board_string(self):
		sorted_keys = sorted(self.board_state) # sort self.board_state by key e.g.: {"a2": "i", "b2": "o", "b3": "o"}

		result = ""
		for key in sorted_keys: # merge into separatorless string e.g.: a2ib2ob3o
			result += (key + self.board_state[key]) # append the concatenated key and value to the result string

		return result

	def get_tile_state(self, column, row):
		assert (column in VALID_COLUMNS)
		assert (row in VALID_ROWS)

		try:
			return self.board_state[(column + row)]
		except KeyError:
			return DEFAULT_TILE_STATE

	def set_player_move(self, column, row):
		self.move_history.append((self.to_board_string(), (column, row))) # append to the move history in the format (board_string, (column, row))
		self._set_tile_state(column, row, 'i') # set the tile to the player's symbol

	def set_opponent_move(self, column, row):
		self._set_tile_state(column, row, 'o') # set the tile to the opponent's symbol

	def _set_tile_state(self, column, row, tile_state):
		assert (column in VALID_COLUMNS)
		assert (row in VALID_ROWS)
		assert (tile_state in VALID_TILE_STATES)

		if tile_state == DEFAULT_TILE_STATE: # if we are setting the tile to the default state
			try:
				del self.board_state[(column + row)] # delete it -- get_tile_state() will handle returning the default state
				return True # success (changes made)
			except KeyError: # if the tile at the row and column specified is already blank
				return False # failure (no changes made)
		else:
			self.board_state[(column + row)] = tile_state # set the state at the given tile
			return True # success # TODO: make sure that changes were actually made

	def get_move_history(self):
		return self.move_history

	def get_legal_moves(self):
		'''Return a list of tuples in the format (column, row) of legal moves for this board'''
		# Note: for tic-tac-toe, legal moves are independent of which side is making the move; this is different for other games
		result = []
		for column in VALID_COLUMNS:
			for row in VALID_ROWS:
				if self.get_tile_state(column, row) == DEFAULT_TILE_STATE:
					result.append((column, row))

		return result

	def get_result(self):
		results = { # define results depending on which tile state 'won' the board
			'i': Result.WIN,
			'o': Result.LOSS
		}

		for column in VALID_COLUMNS: # check for vertical wins
			column_states = [self.get_tile_state(column, row) for row in VALID_ROWS]
			if all(state == column_states[0] for state in column_states): # if all the states for this column are the same
				state = column_states[0] # the first column state is the state of each tile in this column
				if state != DEFAULT_TILE_STATE: # if the column is filled out with a non-default state (i.e. not just blank)
					return results[state] # return the winner of the board based on the dict

		for row in VALID_ROWS: # check for horizontal wins
			row_states = [self.get_tile_state(column, row) for column in VALID_COLUMNS]
			if all(state == row_states[0] for state in row_states):
				state = row_states[0]
				if state != DEFAULT_TILE_STATE:
					return results[state]

		for case in SPECIAL_WIN_CASES: # check for special case wins (diagonals as of current revision)
			case_states = [self.get_tile_state(column, row) for (column, row) in case]
			if all(state == case_states[0] for state in case_states):
				state = case_states[0]
				if state != DEFAULT_TILE_STATE:
					return results[state]

		if len(self.board_state) == (len(VALID_COLUMNS) * len(VALID_ROWS)): # if there are as many tiles set as there are tiles on the board (i.e. board is full but no winner)
			return Result.DRAW # the match is a draw

		return None # no result for this board in its current state


def get_weight(wins, losses, draws):
	'''Calculate the probabilistic weight of a move, given previous experience with it'''
	sample_size = sum((wins, losses, draws))

	if sample_size == 0:
		return 0.5 # if no previous experience, return a default value of 0.5

	sample_proportion = max((wins / sample_size), 0.2) # allow the sample proportion a minimum value of 0.2, to avoid instantly discarding moves that lose their inital game
	return stats.upper_bound_confidence_interval(sample_proportion, sample_size)

def select_move(move_weights):
	'''Randomly select a move from move_weights, taking into consideration their weighted probabilities'''
	# NOTE: in "competition mode", once a high degree of confidence has been established for most possible moves, the highest weight value should be chosen
	# in "learning mode", randomly select a move with respect to the weights, so that new moves may be explored
	return random.choices(list(move_weights.keys()), weights = move_weights.values())[0] # requires Python >=3.6

def get_next_move(board, database):
	legal_moves = board.get_legal_moves()
	known_moves = database.retrieve_move_records(board) # retrieve previously experienced moves with this Board-state and their win-loss-draw records
	# known_moves format: {(column, row): (wins, losses, draws), ...}
	move_weights = {}
	for move in legal_moves: # move = (column, row) TODO: dict comprehension?
		if move in known_moves:
			wins, losses, draws = known_moves[move]
			move_weights[move] = get_weight(wins = wins, losses = losses, draws = draws)
		else:
			move_weights[move] = get_weight(wins = 0, losses = 0, draws = 0)

	return select_move(move_weights)

def dump_move_history(board, result, database):
	'''Record all the archived board states and moves to the database, with the given result attached'''
	move_history = board.get_move_history() # get the board's move history in the format [(board_string, (column, row)), ...]
	for (board_string, (column, row)) in move_history:
		database.increment_move_record(board_string, column, row, result) # TODO: URGENT: optimize this with a batch query at the DatabaseManager level

def handle_check_for_win(player1, player2, database):
	match_result = player1.get_result()  # do a win condition check from Player 1's perspective
	if match_result is not None:
		if match_result == Result.WIN: #  if Player 1 won this match
			print("Player 1 wins!") # TODO: remove debug message for speed
			dump_move_history(player1, Result.WIN, database)
			dump_move_history(player2, Result.LOSS, database)
			return True # the match is complete
		elif match_result == Result.DRAW:
			print("Player 1 and Player 2 draw!") # TODO: remove debug message for speed
			dump_move_history(player1, Result.DRAW, database)
			dump_move_history(player2, Result.DRAW, database)
			return True
		elif match_result == Result.LOSS:
			print("Player 2 wins!") # TODO: remove debug message for speed
			dump_move_history(player1, Result.LOSS, database)
			dump_move_history(player2, Result.WIN, database)
			return True
	return False # the match is not complete yet

def main():
	database = db.DatabaseManager()

	for i in range(100): # play 100 matches
		player1 = Board()
		player2 = Board()
		while True:
			player_1_move = get_next_move(player1, database) # let the AI select Player 1's move
			player1.set_player_move(*player_1_move) # apply the move to Player 1's board
			player2.set_opponent_move(*player_1_move) # apply the move to Player 2's board as well (this time as opponent)

			if handle_check_for_win(player1, player2, database): # if the match is complete after this move
				break # end the match, start a new one if applicable

			player_2_move = get_next_move(player2, database) # let the AI select Player 2's move for its turn
			player1.set_opponent_move(*player_2_move)
			player2.set_player_move(*player_2_move)

			if handle_check_for_win(player1, player2, database):
				break

main()
