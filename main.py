
VALID_COLUMNS		 = ('a', 'b', 'c')
VALID_ROWS			 = ('1', '2', '3')
VALID_TILE_STATES	 = ('b', 'x', 'o') # b = blank

DEFAULT_TILE_STATE	 = 'b'

class Board:

	def __init__(initial_state):
		if initial_state is None:
			self.board_state = []
		else:
			self.board_state = initial_state # TODO: verify

	@staticmethod
	def from_board_string(board_string):
		pass # TODO: restore Board state from a string returned by to_board_string()

	def to_board_string(self):
		pass # TODO: generate a string representing this Board's state

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
			self.board_state[(column + row)] # set the state at the given tile
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
