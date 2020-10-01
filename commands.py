import datetime, sys
from database import DatabaseManager

dbm = DatabaseManager('bookmarks.db')


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
    def execute(self, data):
        data['date_added'] = datetime.datetime.utcnow().isoformat()
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

class QuitCommand:
    def execute(self):
        sys.exit()


if __name__=='__main__':
    command = ListBookmarkCommand()
    selection = command.execute()
    print(selection)