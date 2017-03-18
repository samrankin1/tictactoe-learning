
class DatabaseManager:
	def __init__():
		self.initialize_database()

	def initialize_database():
		'''Create necessary database tables if they don't already exist'''
		# TODO: database sanity checks
		pass # TODO: implement

	def retrieve_move_records(board):
		'''Retrieve all win-loss-draw records associated with moves related to the given Board-state'''
		# SQL: SELECT * FROM `records` WHERE `board_string` = board
		# return format: {(column, row): (wins, losses, draws), ...}
		pass
