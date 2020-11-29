"""
Script to simulate Databases
"""

from database import create_table, add_entry, get_entries

menu = '''Please select one of the following options:
1. Add new entry for today.
2. View entries.
3. Exit.

Your selection: '''

welcome = 'Welcome to this Application'
create_table()

def prompt_new_entry():
    print('Adding new entry ...')

    entry_content = input('What have you learned today?\n')
    entry_date = input('Enter the date: ')

    add_entry(entry_content, entry_date)

def view_entries(entries):
    print('Viewing entries ...')
    print('-------------------')

    for idx, entry in enumerate(entries):
        print(entry['date'])
        print(entry['content'])
        
        if idx != len(entries) - 1:
            print('\n')
    
    print('-------------------')

print(welcome)

user_input = input(menu)

while user_input != '3':

    if user_input == '1':
        prompt_new_entry()
    elif user_input == '2':
        view_entries(get_entries())
    else:
        print('Invalid input. Please try again ...')

    user_input = input(menu)
