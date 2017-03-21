import pymysql
import pymysql.cursors

from main import Result

MYSQL_HOST = 'localhost'
MYSQL_DB = 'test'
MYSQL_USER = 'testuser'
MYSQL_PASS = 'password123'

INITIALIZE_TABLE_SQL		 = ("CREATE TABLE IF NOT EXISTS move_records ( ",
								"`board` VARCHAR(27) NOT NULL, ",
								"`move_column` VARCHAR(1) NOT NULL, ", # TODO: enum
								"`move_row` VARCHAR(1) NOT NULL, " # TODO: enum
								"`wins` UNSIGNED INT NOT NULL DEFAULT 0, ",
								"`losses` UNSIGNED INT NOT NULL DEFAULT 0, ",
								"`draws` UNSIGNED INT NOT NULL DEFAULT 0, ",
								"PRIMARY KEY (`board`, `move_column`, `move_row`)",
								" )ENGINE=InnoDB")

INCREMENT_MOVE_WINS_SQL		 = ("REPLACE INTO move_records(`board`, `move_column`, `move_row`, `wins`) ",
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, (`wins` + 1))")

INCREMENT_MOVE_LOSSES_SQL	 = ("REPLACE INTO move_records(`board`, `move_column`, `move_row`, `losses`) ",
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, (`losses` + 1))")

INCREMENT_MOVE_DRAWS_SQL	 = ("REPLACE INTO move_records(`board`, `move_column`, `move_row`, `draws`) ",
								"VALUES (%(board)s, %(move_column)s, %(move_row)s, (`draws` + 1))")

GET_MOVES_FOR_BOARD_SQL		 = ("SELECT `move_column`, `move_row`, `wins, `losses`, `draws` FROM move_records WHERE `board` = %(board)s", )

class DatabaseManager:
	def __init__():
		self.initialize_database()

	def initialize_database(self):
		'''Create necessary database tables if they don't already exist'''
		self.connection = pymysql.connect(host = MYSQL_HOST,
										user = MYSQL_USER,
										password = MYSQL_PASS,
										db = MYSQL_DB,
										cursorclass = pymysql.cursors.DictCursor)

		with self.connection.cursor() as cursor:
			cursor.execute(INITIALIZE_TABLE_SQL)

		# TODO: database sanity checks

	def increment_move_record(self, board, move_column, move_row, result):
		'''Increment a record in the database for the given board, column, and row for the given result'''
		values = {
			'board': board.to_board_string(),
			'move_column': move_column,
			'move_row': move_row,
		}

		query = {
			Result.WIN:		 INCREMENT_MOVE_WINS_SQL,
			Result.LOSS:	 INCREMENT_MOVE_LOSSES_SQL,
			Result.DRAW:	 INCREMENT_MOVE_DRAWS_SQL
		}[result] # get the correct incrementing SQL query based on the result

		with self.connection.cursor() as cursor:
			cursor.execute(query, values) # execute the incrementing query TODO: catch exceptions, return success

	def retrieve_move_records(self, board):
		'''Retrieve all win-loss-draw records associated with moves related to the given Board-state'''
		# return format: {(column, row): (wins, losses, draws), ...}
		values = {
			'board': board
		}

		with self.connection.cursor() as cursor:
			results = cursor.execute(SELECT_MOVES_FOR_BOARD_SQL, values).fetchall()
			print(results) # TODO: debug
			# return {(column, row): (wins, losses, draws) for (column, row, wins, losses, draws) in results} # TODO: catch exceptions, return success


	def close(self):
		self.connection.close() # close the underlying database connection
