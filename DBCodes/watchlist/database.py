"""
Script to contain and operate the Database Queries for the application
"""

import datetime
import sqlite3

# Queries
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
                                                            title TEXT,
                                                            release_timestamp REAL,
                                                            watched INTEGER
                                                            );"""

INSERT_MOVIES = """INSERT INTO movies (title, release_timestamp, watched) VALUES (?, ?, 0);"""
SELECT_ALL_MOVIES = """SELECT * FROM movies;"""
SELECT_UPCOMING_MOVIES = """SELECT * FROM movies WHERE release_timestamp > ?;"""
SELECT_WATCHED_MOVIES = """SELECT * FROM movies WHERE watched = 1;"""
SET_MOVIE_WATCHED = """UPDATE movies SET watched = 1 WHERE title = ?;"""

# Database
connection = sqlite3.connect('../../Database/data.db')
connection.row_factory = sqlite3.Row    # For Dictionary Style Payload


# Functionalities
def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)

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

def mark_watched(title):
    with connection:
        connection.execute(SET_MOVIE_WATCHED, (title,))

def get_watched_movies():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        
        return cursor.fetchall()

