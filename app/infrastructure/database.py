import sqlite3
from typing import Optional

from app.config import DATABASE_FILE


def start_users_database_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_FILE)
    return conn


def create_users_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT
    )
    """
    cursor.execute(create_statement)
    
    cursor.close()
    connection.commit()

def create_music_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    musics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        genre TEXT,
        image_url TEXT
    )
    """
    cursor.execute(create_statement)
    
    cursor.close()
    connection.commit()

def register_music(connection: sqlite3.Connection, title: str, artist: str, genre: str, image_url: str) -> Optional[int]:
    cursor = connection.cursor()

    insert_statement = """
    INSERT INTO musics (title, artist, genre, image_url)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert_statement, (title, artist, genre, image_url))
    
    inserted_music_id = cursor.lastrowid
    cursor.close()

    connection.commit()
    return inserted_music_id


def create_playlists_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """
    cursor.execute(create_statement)
    
    cursor.close()
    connection.commit()

def create_playlist_music_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    playlist_music (
        playlist_id INTEGER,
        music_id INTEGER,
        FOREIGN KEY (playlist_id) REFERENCES playlists (id),
        FOREIGN KEY (music_id) REFERENCES musics (id)
    )
    """
    cursor.execute(create_statement)
    
    cursor.close()
    connection.commit()
