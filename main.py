from enum import Enum

VALID_COLUMNS		 = ('a', 'b', 'c')
VALID_ROWS			 = ('1', '2', '3')
VALID_TILE_STATES	 = ('b', 'i', 'o') # b = blank, i = controlled by me (X/O), o = controlled by opponent (X/O)

DEFAULT_TILE_STATE	 = 'b'

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

	@staticmethod
	def from_board_string(board_string):
		# separate into groups of three chars
		# e.g.: ["a2i", "b2o", "b3o"]
		# reconstruct the board_state dict
		# e.g.: {"a2": "i", "b2": "o", "b3": "o"}
		pass # TODO: restore Board state from a string returned by to_board_string()

	def to_board_string(self):
		# sort self.board_state by key
		# e.g.: {"a2": "i", "b2": "o", "b3": "o"}
		# merge into separatorless string
		# e.g.: a2ib2ob3o
		sorted_keys = sorted(self.board_state)

		result = ""
		for key in sorted_keys:
			result += (key + self.board_state[key]) # append the concatenated key and value to the result string

		return result

	def get_tile_state(self, column, row):
		if column not in VALID_COLUMNS:
			pass # TODO: throw exception
		if row not in VALID_ROWS:
			pass # TODO: throw exception

		try:
			return self.board_state[(column + row)]
		except KeyError:
			return DEFAULT_TILE_STATE

	def set_tile_state(self, column, row, tile_state):
		if column not in VALID_COLUMNS:
			pass # TODO: throw exception
		if row not in VALID_ROWS:
			pass # TODO: throw exception
		if tile_state not in VALID_TILE_STATES:
			pass # TODO: throw exception

		if tile_state == DEFAULT_TILE_STATE: # if we are setting the tile to the default state
			try:
				del self.board_state[(column + row)] # delete it -- get_tile_state() will handle returning the default state
				return True # success (changes made)
			except KeyError: # if the tile at the row and column specified is already blank
				return False # failure (no changes made)
		else:
			self.board_state[(column + row)] = tile_state # set the state at the given tile
			return True # success # TODO: make sure that changes were actually made

def get_legal_moves(board):
	'''Given a Board object, returns a list of tuples in the format (column, row) of legal moves'''
	# Note: for tic-tac-toe, legal moves are independent of which side is making the move; this is different for other games
	result = []
	for column in VALID_COLUMNS:
		for row in VALID_ROWS:
			if board.get_tile_state(column, row) == DEFAULT_TILE_STATE:
				result.append((column, row))

	return result

def get_weight(wins, losses, draws):
	'''Calculate the probabilistic weight of a move, given previous experience with it'''
	# assign weight according to previous experience (confidence interval? give respect to both results and count)
	# also: define default weight for no previous knowledge (curiousness factor)
	# note: if this algorithm is too 'curious', the program will learn to play against sloppy opponents
	pass # TODO: implement

def select_move(move_weights):
	'''Randomly select a move from move_weights, taking into consideration their weighted probabilities'''
	pass # TODO: implement

def get_next_move(side, board):
	legal_move = get_legal_moves(board)
	# known_moves = database.retrieve_move_records(board) # retrieve previously experienced moves with this Board-state and their win-loss-draw records
	# known_moves format: {(column, row): (wins, losses, draws), ...}
	# move_weights = {}
	for move in legal_moves: # move = (column, row)
		# if move in known_moves
			# wins, losses, draws = known_moves[move]
			# move_weights[move] = get_weight(wins = known_move.wins, losses = known_move.losses, draws = known_move.draws)
		# else
			# move_weights[move] = get_weight(wins = 0, losses = 0, draws = 0)
		pass # TODO: implement

	# return select_move(move_weights)
