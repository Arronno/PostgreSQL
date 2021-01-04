"""
Script to contain and operate the Database Queries for the application
"""

import datetime
import sqlite3

# Queries
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
                                                            id INTEGER PRIMARY KEY,
                                                            title TEXT,
                                                            release_timestamp REAL
                                                            );"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
                                                        username TEXT PRIMARY KEY
                                                        );"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""


CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
                                                                watcher_name TEXT,
                                                                title TEXT
                                                                );"""

INSERT_MOVIES = """INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"""
SELECT_ALL_MOVIES = """SELECT * FROM movies;"""
SELECT_UPCOMING_MOVIES = """SELECT * FROM movies WHERE release_timestamp > ?;"""

SELECT_WATCHED_MOVIES = """SELECT movies.*
FROM movies
JOIN watched ON watched.movie_id = movies.id
JOIN users ON users.username = watched.user_username
WHERE users.username = ?;
"""

DELETE_MOVIE = """DELETE FROM movies WHERE title = ?;"""
INSERT_WATCHED_MOVIE = """INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"""
INSERT_USER = """INSERT INTO users (username) VALUES (?)"""
SEARCH_MOVIE = """SELECT * FROM movies WHERE title LIKE ?;"""
CREATE_RELEASE_INDEX = """CREATE INDEX idx_movies_release ON movies(release_timestamp);"""

# Database
connection = sqlite3.connect('../../Database/data.db')
connection.row_factory = sqlite3.Row    # For Dictionary Style Payload


# Functionalities
def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)

def add_movies(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))

def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()

        if upcoming:
            now_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (now_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)

        return cursor.fetchall()

def search_movies(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
        return cursor.fetchall()

def mark_watched(username, movie_id):
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))

def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        
        return cursor.fetchall()

def add_user(username):
    with connection:
        connection.execute(INSERT_USER, (username,))
        