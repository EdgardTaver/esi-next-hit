import sqlite3
from typing import Optional

import pandas as pd

from app.backend.config import DATABASE_FILE, MUSICS_CSV_FILE


def start_users_database_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_FILE)
    return conn


def create_users_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    create_statement = """
    CREATE TABLE IF NOT EXISTS
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        playlist_id INTEGER,
        music_id INTEGER,
        FOREIGN KEY (playlist_id) REFERENCES playlists (id),
        FOREIGN KEY (music_id) REFERENCES musics (id)
    )
    """
    cursor.execute(create_statement)
    
    cursor.close()
    connection.commit()

def database_setup(connection: sqlite3.Connection):
    create_users_table(connection)
    create_music_table(connection)
    create_playlists_table(connection)
    create_playlist_music_table(connection)

def database_fill_up_musics_table(connection: sqlite3.Connection):
    cursor = connection.cursor()

    select_musics = """
    SELECT COUNT(*) FROM musics
    """

    cursor.execute(select_musics)
    musics_count = cursor.fetchone()[0]

    if musics_count == 0:
        musics_df = pd.read_csv(MUSICS_CSV_FILE)
        musics_df.to_sql("musics", connection, if_exists="append", index=False)

    cursor.close()