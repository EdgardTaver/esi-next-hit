import sqlite3
from typing import List, Optional

from app.exceptions import (EmailAlreadyRegisteredException,
                            MusicAlreadyInPlaylistException,
                            MusicNotFoundException,
                            PlaylistAlreadyExistsException,
                            PlaylistNotFoundException)
from app.infrastructure.password import encrypt_password


def register_user(connection: sqlite3.Connection, email: str, password: str, name:str) -> Optional[int]:
    cursor = connection.cursor()

    select_statement = """
    SELECT email FROM users WHERE email=?
    """

    cursor.execute(select_statement, (email,))
    result = cursor.fetchone()

    if result is not None:
        raise EmailAlreadyRegisteredException()

    insert_statement = """
    INSERT INTO users (email, password, name)
    VALUES (?, ?, ?)
    """

    encrypted_password = encrypt_password(password)
    cursor.execute(insert_statement, (email, encrypted_password, name))
    connection.commit()

    inserted_user_id = cursor.lastrowid
    cursor.close()

    return inserted_user_id


def get_authenticated_user_id(connection: sqlite3.Connection, email: str, password: str) -> Optional[int]:
    cursor = connection.cursor()

    cursor.execute("SELECT id, password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        user_id, stored_password = result
        if encrypt_password(password) == stored_password:
            return user_id

    return None


def register_playlist(connection: sqlite3.Connection, name: str, user_id: int) -> Optional[int]:
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
    
    inserted_playlist_id = cursor.lastrowid
    cursor.close()

    return inserted_playlist_id

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
    cursor.close()
    connection.commit()

def list_playlists_for_user(connection: sqlite3.Connection, user_id: int):
    cursor = connection.cursor()

    select_playlists_statement = """
    SELECT * FROM playlists WHERE user_id=?
    """
    cursor.execute(select_playlists_statement, (user_id,))
    
    names = [description[0] for description in cursor.description]
    results = [dict(zip(names, row)) for row in cursor.fetchall()]

    cursor.close()
    return results

def list_musics_in_playlist(connection: sqlite3.Connection, playlist_id: int):
    cursor = connection.cursor()

    select_musics_statement = """
    SELECT * FROM playlist_music
    INNER JOIN musics ON playlist_music.music_id=musics.id
    WHERE playlist_id=?
    """
    cursor.execute(select_musics_statement, (playlist_id,))
    
    names = [description[0] for description in cursor.description]
    results = [dict(zip(names, row)) for row in cursor.fetchall()]

    cursor.close()
    return results

def list_suggestions_for_user():
    """
    SELECT * FROM musics
    INNER JOIN playlist_music ON musics.id=playlist_music.music_id
    INNER JOIN playlists ON playlist_music.playlist_id=playlists.id
    WHERE playlists.user_id=?
    """

def search_music(connection: sqlite3.Connection, search_string: str):
    cursor = connection.cursor()

    select_music_statement = """
    SELECT * FROM musics WHERE title LIKE ?
    ORDER BY LOWER(title) ASC, id ASC
    LIMIT 10
    """
    cursor.execute(select_music_statement, ('%' + search_string + '%',))
    
    names = [description[0] for description in cursor.description]
    results = [dict(zip(names, row)) for row in cursor.fetchall()]

    cursor.close()
    return results

def list_genres_for_user(connection: sqlite3.Connection, user_id: int) -> List[str]:
    cursor = connection.cursor()

    select_statement = """
    SELECT distinct(musics.genre) FROM musics
    INNER JOIN playlist_music ON musics.id=playlist_music.music_id
    INNER JOIN playlists ON playlist_music.playlist_id=playlists.id
    WHERE playlists.user_id=?
    ORDER BY 1 ASC
    """

    cursor.execute(select_statement, (user_id,))

    results = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return results

def list_music_ids_for_user(connection: sqlite3.Connection, user_id: int) -> List[int]:
    cursor = connection.cursor()

    select_statement = """
    SELECT musics.id FROM musics
    INNER JOIN playlist_music ON musics.id=playlist_music.music_id
    INNER JOIN playlists ON playlist_music.playlist_id=playlists.id
    WHERE playlists.user_id=?
    ORDER BY 1 ASC
    """

    cursor.execute(select_statement, (user_id,))

    results = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return results

def get_music_recommendations_for_user(connection: sqlite3.Connection, user_id: int):
    genre_list = list_genres_for_user(connection, user_id)
    known_music_ids = list_music_ids_for_user(connection, user_id)

    if len(genre_list) == 0 or len(known_music_ids) == 0:
        return get_any_random_musics(
            connection)
        # get any 5 random musics
        # since we only know the user tastes by the musics in their playlists
        # if there are no playlists, then the user is totally new and a random
        # guess is our best guess

    else:
        return get_random_new_musics_for_the_genres_the_user_listens_to(
            connection, genre_list, known_music_ids)

def get_any_random_musics(connection: sqlite3.Connection):
    cursor = connection.cursor()

    select_statement = """
    SELECT * FROM musics
    ORDER BY RANDOM()
    LIMIT 5
    """

    cursor.execute(select_statement)

    names = [description[0] for description in cursor.description]
    results = [dict(zip(names, row)) for row in cursor.fetchall()]
    cursor.close()

    return results

def get_random_new_musics_for_the_genres_the_user_listens_to(connection: sqlite3.Connection, genre_list: List[str], known_music_ids: List[int]):
    cursor = connection.cursor()

    select_statement = """
    SELECT * FROM musics
    WHERE 1=1
    AND genre IN ({})
    AND id NOT IN ({})
    ORDER BY RANDOM()
    LIMIT 5
    """

    formatted_genre_list = ','.join('?' * len(genre_list))
    formatted_known_music_ids = ','.join('?' * len(known_music_ids))

    cursor.execute(
        select_statement.format(formatted_genre_list, formatted_known_music_ids),
        genre_list + known_music_ids)

    names = [description[0] for description in cursor.description]
    results = [dict(zip(names, row)) for row in cursor.fetchall()]
    cursor.close()

    return results
