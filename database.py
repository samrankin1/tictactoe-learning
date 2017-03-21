import pymysql
import pymysql.cursors

MYSQL_HOST = 'localhost'
MYSQL_DB = 'test'
MYSQL_USER = 'testuser'
MYSQL_PASS = 'password123'


INITIALIZE_TABLE_SQL		 = ("CREATE TABLE IF NOT EXISTS move_records ( ",
								"`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ",
								"`board` VARCHAR(27) NOT NULL, ",
								"`move_column` VARCHAR(1) NOT NULL, ", # TODO: enum
								"`move_row` VARCHAR(1) NOT NULL, " # TODO: enum
								"`wins` UNSIGNED INT NOT NULL, ",
								"`losses` UNSIGNED INT NOT NULL, ",
								"`draws` UNSIGNED INT NOT NULL, ",
								" )ENGINE=InnoDB")

INSERT_MOVE_FOR_BOARD_SQL	 = ("INSERT INTO move_records(`board`, `move_column`, `move_row`, `wins`, `losses`, `draws`) ",
								"VALUES (%(board)s, %(move_column), %(move_row), %(wins), %(losses), %(draws))")

SELECT_MOVES_FOR_BOARD_SQL	 = ("SELECT `move_column`, `move_row`, `wins, `losses`, `draws` FROM move_records WHERE `board` = %(board)s", )


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

	def insert_move_record(self, board, move_column, move_row, result):


	def retrieve_move_records(self, board):
		'''Retrieve all win-loss-draw records associated with moves related to the given Board-state'''
		# SQL: SELECT * FROM `records` WHERE `board_string` = board
		# return format: {(column, row): (wins, losses, draws), ...}
		pass

	def close(self):
		self.connection.close() # close the underlying database connection
