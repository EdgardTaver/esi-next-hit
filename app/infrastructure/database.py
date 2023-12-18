import sqlite3
from typing import Optional

from app.config import DATABASE_FILE
from app.exceptions import (EmailAlreadyRegisteredException, MusicAlreadyInPlaylistException, MusicNotFoundException,
                            PlaylistAlreadyExistsException, PlaylistNotFoundException)
from app.infrastructure.password import encrypt_password


def start_users_database_connection() -> sqlite3.Connection:
    # TODO: integration test?
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
    connection.commit()

def register_music(connection: sqlite3.Connection, title: str, artist: str, genre: str, image_url: str) -> int:
    # TODO: add testing
    cursor = connection.cursor()

    insert_statement = """
    INSERT INTO musics (title, artist, genre, image_url)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert_statement, (title, artist, genre, image_url))
    connection.commit()
    
    inserted_music_id = cursor.lastrowid
    cursor.close()

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
    connection.commit()


def register_user(connection: sqlite3.Connection, email: str, password: str):
    cursor = connection.cursor()

    select_statement = """
    SELECT email FROM users WHERE email=?
    """

    cursor.execute(select_statement, (email,))
    result = cursor.fetchone()

    if result is not None:
        raise EmailAlreadyRegisteredException()

    insert_statement = """
    INSERT INTO users (email, password)
    VALUES (?, ?)
    """

    encrypted_password = encrypt_password(password)
    cursor.execute(insert_statement, (email, encrypted_password))
    connection.commit()

def get_authenticated_user_id(connection: sqlite3.Connection, email: str, password: str) -> Optional[int]:
    cursor = connection.cursor()

    cursor.execute("SELECT id, password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        user_id, stored_password = result
        if encrypt_password(password) == stored_password:
            return user_id

    return None
