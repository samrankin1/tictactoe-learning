import pymysql
import pymysql.cursors

import main

MYSQL_HOST = 'localhost'
MYSQL_DB = 'tictactoe'
MYSQL_USER = 'tictactoe'
MYSQL_PASS = 'password123'

INITIALIZE_TABLE_SQL		 = ("CREATE TABLE IF NOT EXISTS move_records ( "
								"`board` VARCHAR(27) NOT NULL, "
								"`move_column` VARCHAR(1) NOT NULL, " # TODO: enum
								"`move_row` VARCHAR(1) NOT NULL, " # TODO: enum
								"`wins` INT UNSIGNED NOT NULL DEFAULT 0, "
								"`losses` INT UNSIGNED NOT NULL DEFAULT 0, "
								"`draws` INT UNSIGNED NOT NULL DEFAULT 0, "
								"PRIMARY KEY (`board`, `move_column`, `move_row`)"
								" )ENGINE=InnoDB")

INCREMENT_MOVE_WINS_SQL		 = ("INSERT INTO move_records(`board`, `move_column`, `move_row`, `wins`) "
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, 1) "
								"ON DUPLICATE KEY UPDATE `wins` = (`wins` + 1)")

INCREMENT_MOVE_LOSSES_SQL	 = ("INSERT INTO move_records(`board`, `move_column`, `move_row`, `losses`) "
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, 1) "
								"ON DUPLICATE KEY UPDATE `losses` = (`losses` + 1)")

INCREMENT_MOVE_DRAWS_SQL	 = ("INSERT INTO move_records(`board`, `move_column`, `move_row`, `draws`) "
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, 1) "
								"ON DUPLICATE KEY UPDATE `draws` = (`draws` + 1)")

GET_MOVES_FOR_BOARD_SQL		 = "SELECT `move_column`, `move_row`, `wins`, `losses`, `draws` FROM move_records WHERE `board` = %(board)s"

class DatabaseManager:
	def __init__(self):
		self._initialize_database()

	def _initialize_database(self):
		'''Create necessary database tables if they don't already exist'''
		self.connection = pymysql.connect(host = MYSQL_HOST,
										user = MYSQL_USER,
										password = MYSQL_PASS,
										db = MYSQL_DB,
										autocommit = True,
										cursorclass = pymysql.cursors.DictCursor)

		with self.connection.cursor() as cursor:
			cursor.execute(INITIALIZE_TABLE_SQL)

		# TODO: database sanity checks

	def increment_move_record(self, board_string, move_column, move_row, result):
		'''Increment a record in the database for the given board, column, and row for the given result'''
		values = {
			'board': board_string,
			'move_column': move_column,
			'move_row': move_row,
		}

		print(result) # TODO: debug
		query = {
			main.Result.WIN:		 INCREMENT_MOVE_WINS_SQL,
			main.Result.LOSS:	 INCREMENT_MOVE_LOSSES_SQL,
			main.Result.DRAW:	 INCREMENT_MOVE_DRAWS_SQL
		}[result] # get the correct incrementing SQL query based on the result

		with self.connection.cursor() as cursor:
			cursor.execute(query, values) # execute the incrementing query TODO: catch exceptions, return success

	def retrieve_move_records(self, board):
		'''Retrieve all win-loss-draw records associated with moves related to the given Board-state'''
		# return format: {(column, row): (wins, losses, draws), ...} # NOTE: this could be a list of tuples?
		values = {
			'board': board.to_board_string()
		}

		with self.connection.cursor() as cursor:
			results = cursor.execute(GET_MOVES_FOR_BOARD_SQL, values)
			return {(result['move_column'], result['move_row']): (result['wins'], result['losses'], result['draws']) for result in cursor.fetchall()} # TODO: catch exceptions, return success

	def close(self):
		self.connection.close() # close the underlying database connection
