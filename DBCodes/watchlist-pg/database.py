"""
Script to contain and operate the Database Queries for the application
"""

import os
import datetime
import psycopg2
import psycopg2.extras      # Must import separately to work with cursor_factory

from dotenv import load_dotenv

load_dotenv()

# Queries
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
                                                            id SERIAL PRIMARY KEY,
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

INSERT_MOVIES = """INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"""
SELECT_ALL_MOVIES = """SELECT * FROM movies;"""
SELECT_UPCOMING_MOVIES = """SELECT * FROM movies WHERE release_timestamp > %s;"""

SELECT_WATCHED_MOVIES = """SELECT movies.*
FROM movies
JOIN watched ON watched.movie_id = movies.id
JOIN users ON users.username = watched.user_username
WHERE users.username = %s;
"""

DELETE_MOVIE = """DELETE FROM movies WHERE title = %s;"""
INSERT_WATCHED_MOVIE = """INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"""
INSERT_USER = """INSERT INTO users (username) VALUES (%s)"""
SEARCH_MOVIE = """SELECT * FROM movies WHERE title LIKE %s;"""
CREATE_RELEASE_INDEX = """CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"""

# Database
connection = psycopg2.connect(os.environ['DATABASE_URL'])
connection.cursor_factory = psycopg2.extras.RealDictCursor    # For Dictionary Style Payload


# Functionalities
def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)

def add_movies(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))

def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:

            if upcoming:
                now_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (now_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)

            return cursor.fetchall()

def search_movies(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
            return cursor.fetchall()

def mark_watched(username, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))

def get_watched_movies(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        
            return cursor.fetchall()

def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))
