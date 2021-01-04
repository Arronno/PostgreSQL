import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Add user to the app.
7) Search for a movie.
8) Exit.

Your selection: """

welcome = "Welcome to the Watchlist app!"

print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input('Movie Title: ')
    release_date = input('Release Date (dd-mm-YYYY): ')
    parsed_date = datetime.datetime.strptime(release_date, '%d-%m-%Y')
    release_timestamp = parsed_date.timestamp()

    database.add_movies(title, release_timestamp)

def print_movie_list(heading, movies):
    print(f'--- {heading} Movies ---')
    for movie in movies:
        _id = movie['id']
        title = movie['title']
        timestamp = movie['release_timestamp']
        readable_date = datetime.datetime.fromtimestamp(timestamp).strftime('%b %d %Y')

        print(f'{_id}: {title} -> Release Date: {readable_date}')
    print('------\n') 

def prompt_mark_watched():
    username = input('Username: ')
    movie_id = input('Enter Watched Movie ID: ')
    database.mark_watched(username, movie_id)

def prompt_add_user():
    username = input('Username: ')
    database.add_user(username)

def prompt_show_watched_movies():
    username = input('Username: ')
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list('Watched', movies)
    else:
        print('No watched movies')

def prompt_search_movies():
    search_term = input('Enter partial movie title: ')
    movies = database.search_movies(search_term)

    if movies:
        print_movie_list('Movies found', movies)
    else:
        print('No movies found')


user_input = input(menu)

while user_input != "8":

    if user_input == "1":
        prompt_add_movie()

    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list('Upcoming', movies)

    elif user_input == "3":
        movies = database.get_movies(False)
        print_movie_list('All', movies)

    elif user_input == "4":
        prompt_mark_watched()

    elif user_input == "5":
        prompt_show_watched_movies()

    elif user_input == "6":
        prompt_add_user()

    elif user_input == "7":
        prompt_search_movies()

    else:
        print('Invalid input, please try again!')

    user_input = input(menu)
