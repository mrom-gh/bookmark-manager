"""DatabaseManager - Constitutes the persistence layer"""

import sqlite3


class DatabaseManager:

	def __init__(self, database_filename):
		self.connection = sqlite3.connect(database_filename)

	def __del__(self):
		self.connection.close()

	def _execute(self, statement, values=None):
		"""Use statements with placeholders for values to prevent sql
		injection.
		"""
		with self.connection:
			cursor = self.connection.cursor()
			cursor.execute(statement, values or [])
			return cursor

	def _format_columns(self, columns):
		# columns = {'id':'INTEGER PRIMARY KEY AUTOINCREMENT', ...}
		columns_with_types = []  # ['id INTEGER PRIMARY KEY AUTOINCREMENT', ...]
		for column_name, data_type in columns.items():
			columns_with_types.append(' '.join([column_name, data_type]))
		return columns_with_types

	def create_table(self, table_name, columns):
		columns_with_types = self._format_columns(columns)
		statement = (
			f'CREATE TABLE IF NOT EXISTS {table_name} ( '
			f'{", ".join(columns_with_types)} '
			');'
		)
		self._execute(statement)

	def drop_table(self, table_name):
		self._execute(f'DROP TABLE {table_name};')

	def _format_data(self, data):
		# data = {'id':2, 'title':'Tolle Seite', ...}
		column_names = ', '.join(data.keys())  # 'id, title, ... '
		placeholders = ', '.join('?' * len(data))  # '?, ?, ...'
		column_values = list(data.values())  # ['2', 'Tolle Seite']
		return column_names, placeholders, column_values

	def add(self, table_name, data):
		column_names, placeholders, column_values = self._format_data(data)
		# query -> INSERT INTO table_name (id, title, ...)
		#          VALUES (?, ?, ...);
		query = (
			f"INSERT INTO {table_name} ({column_names}) "
			f"VALUES ({placeholders});"
		)
		self._execute(query, column_values)

	def _format_criteria(self, criteria):
		# criteria = {'id':2, 'title':'Tolle Seite', ...}
		criteria_w_pl = [f'{column_name} = ?' for column_name in criteria]
		criteria_w_pl = ' AND '.join(criteria_w_pl)  # 'WHERE id=? AND title=?'
		criteria_values = list(criteria.values())  # ['2', 'Tolle Seite', ...]
		return criteria_w_pl, criteria_values

	def delete(self, table_name, criteria):
		criteria_with_placeholders, criteria_values = self._format_criteria(criteria)
		# query -> DELETE FROM table_name WHERE id=? AND title=? AND ...;
		query = f"DELETE FROM {table_name} WHERE {criteria_with_placeholders};"
		self._execute(query, criteria_values)

	def select(self, table_name, criteria={}, order_by='', case_sens=False):
		criteria_with_placeholders, criteria_values = self._format_criteria(criteria)
		# query -> SELECT * FROM table_name (WHERE id=? AND title=? (ORDER BY title));
		query = f"SELECT * FROM {table_name}"
		if criteria: query += f" WHERE {criteria_with_placeholders}"
		if order_by:
			query += f" ORDER BY {order_by} COLLATE NOCASE"
			if case_sens: query = query[:-len(" COLLATE NOCASE")]
		query += ';'
		return self._execute(query, criteria_values)  # fetchall() für liste


if __name__ == '__main__':
    dbm = DatabaseManager('test.db')
    
    columns = {
	'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
	'title': 'TEXT NOT NULL',
	'url': 'TEXT NOT NULL',
	'notes': 'TEXT',
	'date_added': 'TEXT NOT NULL'
    }
    dbm.create_table('bookmarks', columns)
    #dbm.drop_table('bookmarks')

    data = {
	'title': 'SQLITE Tutorial',
	'url': 'www.sqlitetutorial.net',
	'notes': 'Schnelles und gutes Tutorial',
	'date_added': '2020-09-30'
    }
    dbm.add('bookmarks', data)
    
    criteria = {
	'title':'SQLITE Tutorial',
    }
    #dbm.delete('bookmarks', criteria)
    
    criteria = {
	'id':7,
	'title':'SQLITE Tutorial'
    }
    selection = dbm.select('bookmarks')
    #selection = dbm.select('bookmarks', order_by='date_added')
    #selection = dbm.select('bookmarks', order_by='title', case_sens=True)
    #selection = dbm.select('bookmarks', criteria)
    #selection = dbm.select('bookmarks', criteria, order_by='title')
    print(*selection, sep='\n')  # use * to unpack generator