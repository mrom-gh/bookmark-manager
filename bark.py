import os
import commands

class A:
	pass

class Option:

	def __init__(self, name, command, prep_call=None):
		self.name = name
		self.command = command
		self.prep_call = prep_call
    
	def choose(self):
		if self.prep_call: data = self.prep_call()
		else: data = None
	
		if data: message = self.command.execute(data)
		else: message = self.command.execute()
		print(message)
		
	def __str__(self):
		return self.name


def clear_screen():
    clear = 'cls' if os.name=='nt' else 'clear'
    os.system(clear)

def print_options():
	for letter, option in options.items():
		print(f"({letter}) {option}")

def get_option_choice():
	while True:
		letter = input('Choose an option: ').lower()
		if letter in options.keys():
			print()
			return options[letter]
		else:
			print('Invalid choice... choose again')


def get_user_input(label, required=True):
	while True:
		user_input = input(f'Enter {label}: ')
		if user_input or not required:
			return user_input

def get_new_bookmark_data():
    return {
	'title':get_user_input('title'),
	'url':get_user_input('url'),
	'notes':get_user_input('notes', required=False),
    }

def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete: ')


def loop():
	while True:
		print_options()
		user_option = get_option_choice()
		print(user_option)
		user_option.choose()
		input('Press ENTER to return to menu')
		print()


if __name__ == '__main__':
    clear_screen()
    print('Welcome to bark!\n')
    
    command = commands.CreateBookmarksTableCommand()
    command.execute()

    options = {
	'a': Option('Add a bookmark',
	            commands.AddBookmarkCommand(),
	            prep_call=get_new_bookmark_data
	     ),
	'b': Option('List bookmarks by date',
	            commands.ListBookmarkCommand()
	     ),
	'c': Option('List bookmarks by title',
	            commands.ListBookmarkCommand(order_by='title')
	     ),
	'd': Option('Delete a bookmark',
	            commands.DeleteBookmarkCommand(),
	            prep_call=get_bookmark_id_for_deletion
	     ),
	'q': Option('Quit', commands.QuitCommand())
    }
    
    loop()