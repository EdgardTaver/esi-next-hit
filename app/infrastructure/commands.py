import sqlite3

from app.exceptions import MusicAlreadyInPlaylistException, MusicNotFoundException, PlaylistNotFoundException


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