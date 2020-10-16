"""Commands module - Constitutes the business logic"""

import datetime, sys
import requests
from database import DatabaseManager

dbm = DatabaseManager('bookmarks.db')

# TODO: Wire ImportGithubStarsCommand with the UI

class CreateBookmarksTableCommand:
	def execute(self):
		columns = {
			'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
			'title': 'TEXT NOT NULL',
			'url': 'TEXT NOT NULL',
			'notes': 'TEXT',
			'date_added': 'TEXT NOT NULL'
		}
		dbm.create_table('bookmarks', columns)

class AddBookmarkCommand:
	# data: part of shared interface with DatabaseManager method "add"
	#       and Options method "choose"
	def execute(self, data, timestamp=None):
		data['date_added'] = timestamp or datetime.datetime.utcnow().isoformat()
		dbm.add('bookmarks', data)
		return 'Bookmark added'

class ListBookmarkCommand:
	def __init__(self, order_by='date_added'):
		self.order_by = order_by
	def execute(self):
		selection = dbm.select('bookmarks', order_by=self.order_by)  # cursor
		selection_formatted = ''
		for item in selection.fetchall():
			selection_formatted += str(item) + '\n'
		return selection_formatted

class DeleteBookmarkCommand:
	def execute(self, bookmark_id):
		criteria = {'id': bookmark_id}
		dbm.delete('bookmarks', criteria)
		return 'Bookmark deleted'

class ImportGithubStarsCommand:
	def __init__(self, token):
		self.token = token
	def _get_list_of_stars(self):
		headers = {'Authorization': f'token {self.token}'}
		print(type(headers), headers)
		response = requests.get('https://api.github.com/user/starred', headers=headers)
		return response.json()  # [{link 1}, {link 2}, ...]
	def _get_new_bookmark_data(self, list_of_stars, i):
		return {
			'title':list_of_stars[i]['full_name'],
			'url': list_of_stars[i]['html_url'],
			'notes':list_of_stars[i]['description'],
		}
	def execute(self):
		list_of_stars = self._get_list_of_stars()
		r = []
		for i in range(len(list_of_stars)):
			data = self._get_new_bookmark_data(list_of_stars, i)
			msg = AddBookmarkCommand().execute(data)
			r.append(msg)
		return ', '.join(r)

class QuitCommand:
	def execute(self):
		sys.exit()


if __name__=='__main__':
	with open('token', encoding='utf-8') as infile:
		token = infile.read().strip()
	command = ImportGithubStarsCommand(token)
	print(command.execute())