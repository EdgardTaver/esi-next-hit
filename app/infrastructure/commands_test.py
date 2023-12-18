
import pytest

from app.exceptions import (MusicAlreadyInPlaylistException,
                            MusicNotFoundException, PlaylistAlreadyExistsException, PlaylistNotFoundException)
from app.infrastructure.commands import (register_music_in_playlist,
                                         register_playlist)
from app.infrastructure.database import (create_music_table,
                                         create_playlist_music_table,
                                         create_playlists_table,
                                         create_users_table, register_music)
from app.testing import start_sqlite_in_memory_database_connection


def test_register_playlist_when_playlist_does_not_exist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_users_table(connection)

    user_id = 1
    playlist_name = "My Playlist"
    exercise = register_playlist(connection, playlist_name, user_id)
    assert exercise == 1

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM playlists WHERE name=?", (playlist_name,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == playlist_name
    assert result[2] == user_id

    cursor.close()


def test_register_playlist_when_playlist_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_users_table(connection)

    user_id = 1
    playlist_name = "My Playlist"
    register_playlist(connection, playlist_name, user_id)

    with pytest.raises(PlaylistAlreadyExistsException):
        register_playlist(connection, playlist_name, user_id)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM playlists WHERE name=? AND user_id=?", (playlist_name, user_id))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()


def test_register_music_in_playlist_when_playlist_not_found():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    invalid_playlist_id = 1
    existing_music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")

    with pytest.raises(PlaylistNotFoundException):
        register_music_in_playlist(connection, invalid_playlist_id, existing_music_id)


def test_register_music_in_playlist_when_music_not_found():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    existing_playlist_id = register_playlist(connection, "My Playlist", 1)
    existing_music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    invalid_music_id = existing_music_id + 1

    with pytest.raises(MusicNotFoundException):
        register_music_in_playlist(connection, existing_playlist_id, invalid_music_id)


def test_register_music_in_playlist_when_music_not_in_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    playlist_id = register_playlist(connection, "My Playlist", 1)
    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")

    register_music_in_playlist(connection, playlist_id, music_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM playlist_music WHERE playlist_id=? AND music_id=?", (playlist_id, music_id))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == playlist_id
    assert result[1] == music_id

    cursor.close()


def test_register_music_in_playlist_when_music_already_in_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    playlist_id = register_playlist(connection, "My Playlist", 1)
    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")

    register_music_in_playlist(connection, playlist_id, music_id)

    with pytest.raises(MusicAlreadyInPlaylistException):
        register_music_in_playlist(connection, playlist_id, music_id)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM playlist_music WHERE playlist_id=? AND music_id=?", (playlist_id, music_id))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()
