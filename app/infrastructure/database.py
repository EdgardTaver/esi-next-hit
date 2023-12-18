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

def register_playlist(connection: sqlite3.Connection, name: str, user_id: int):
    cursor = connection.cursor()

    select_statement = """
    SELECT id FROM playlists WHERE name=? AND user_id=?
    """
    cursor.execute(select_statement, (name, user_id))
    existing_playlist = cursor.fetchone()

    if existing_playlist:
        raise PlaylistAlreadyExistsException("Playlist with the same name already exists for the user")

    insert_statement = """
    INSERT INTO playlists (name, user_id)
    VALUES (?, ?)
    """

    cursor.execute(insert_statement, (name, user_id))
    connection.commit()

def register_music_in_playlist(connection: sqlite3.Connection, playlist_id: int, music_id: int):
    cursor = connection.cursor()

    select_playlist_statement = """
    SELECT id FROM playlists WHERE id=?
    """
    cursor.execute(select_playlist_statement, (playlist_id,))
    existing_playlist = cursor.fetchone()

    if not existing_playlist:
        raise PlaylistNotFoundException("Playlist does not exist")
    
    select_music_statement = """
    SELECT id FROM musics WHERE id=?
    """
    cursor.execute(select_music_statement, (music_id,))
    existing_music = cursor.fetchone()

    if not existing_music:
        raise MusicNotFoundException("Music does not exist")

    select_music_statement = """
    SELECT playlist_id, music_id FROM playlist_music WHERE playlist_id=? AND music_id=?
    """
    cursor.execute(select_music_statement, (playlist_id, music_id))
    existing_music = cursor.fetchone()

    if existing_music:
        raise MusicAlreadyInPlaylistException("Music already in playlist")

    insert_statement = """
    INSERT INTO playlist_music (playlist_id, music_id)
    VALUES (?, ?)
    """

    cursor.execute(insert_statement, (playlist_id, music_id))
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
