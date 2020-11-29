import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

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
        title = movie['title']
        timestamp = movie['release_timestamp']
        readable_date = datetime.datetime.fromtimestamp(timestamp).strftime('%b %d %Y')

        print(f'{title} -> Release Date: {readable_date}')
    print('------\n')

def promp_mark_watched():
    movie_title = input('Enter Watched Movie Title: ')
    database.mark_watched(movie_title)


user_input = input(menu)

while user_input != "6":

    if user_input == "1":
        prompt_add_movie()

    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list('Upcoming', movies)

    elif user_input == "3":
        movies = database.get_movies(False)
        print_movie_list('All', movies)

    elif user_input == "4":
        promp_mark_watched()

    elif user_input == "5":
        movies = database.get_watched_movies()
        print_movie_list('Watched', movies)

    else:
        print('Invalid input, please try again!')

    user_input = input(menu)
