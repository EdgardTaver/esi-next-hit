from app.backend.database import (create_music_table,
                                         create_playlist_music_table,
                                         create_playlists_table,
                                         create_users_table, register_music)
from app.backend.testing import start_sqlite_in_memory_database_connection


def test_create_users_table_when_table_does_not_exist():
    connection = start_sqlite_in_memory_database_connection()
    cursor = connection.cursor()
    
    create_users_table(connection)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    
    cursor.close()

    assert result is not None

def test_create_users_table_when_table_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    try:
        create_users_table(connection)
        assert True
    except Exception:
        assert False, "should not raise exception when table already exists"


def test_create_music_table_when_table_does_not_exist():
    connection = start_sqlite_in_memory_database_connection()
    
    create_music_table(connection)

    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='musics'")
    result = cursor.fetchone()
    
    cursor.close()

    assert result is not None

def test_create_music_table_when_table_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_music_table(connection)

    try:
        create_music_table(connection)
        assert True
    except Exception:
        assert False, "should not raise exception when table already exists"

def test_create_playlists_table_when_table_does_not_exist():
    connection = start_sqlite_in_memory_database_connection()
    
    create_playlists_table(connection)

    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='playlists'")
    result = cursor.fetchone()
    
    cursor.close()

    assert result is not None

def test_create_playlists_table_when_table_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)

    try:
        create_playlists_table(connection)
        assert True
    except Exception:
        assert False, "should not raise exception when table already exists"

def test_create_playlist_music_table_when_table_does_not_exist():
    connection = start_sqlite_in_memory_database_connection()

    create_playlist_music_table(connection)

    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='playlist_music'")
    result = cursor.fetchone()

    cursor.close()

    assert result is not None


def test_create_playlist_music_table_when_table_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_playlist_music_table(connection)

    try:
        create_playlist_music_table(connection)
        assert True
    except Exception:
        assert False, "should not raise exception when table already exists"


def test_register_music_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_music_table(connection)
    
    title = "Test Music"
    artist = "Test Artist"
    genre = "Test Genre"
    image_url = "http://example.com/test.jpg"
    inserted_music_id = register_music(connection, title, artist, genre, image_url)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM musics WHERE id=?", (inserted_music_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == title
    assert result[2] == artist
    assert result[3] == genre
    assert result[4] == image_url

    cursor.close()
