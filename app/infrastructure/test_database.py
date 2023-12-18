import pytest

from app.exceptions import EmailAlreadyRegisteredException
from app.infrastructure.database import (authenticate_user, create_music_table,
                                         create_playlist_music_table,
                                         create_playlists_table,
                                         create_users_table, register_user)
from app.testing import start_sqlite_in_memory_database_connection


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


def test_register_user_when_email_is_new():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    new_email = "test@example.com"
    new_password = "password123"
    register_user(connection, new_email, new_password)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (new_email,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == new_email

    cursor.close()

def test_register_user_when_email_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    new_password = "password456"

    with pytest.raises(EmailAlreadyRegisteredException):
        register_user(connection, existing_email, new_password)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (existing_email,))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()

def test_authenticate_user_when_email_is_not_registered():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    non_existing_email = "cachorro@banana.com"
    any_password = "password456"

    result = authenticate_user(connection, non_existing_email, any_password)
    assert result is None

def test_authenticate_user_when_email_exists_but_password_is_incorrect():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    register_user(connection, existing_email, existing_password)

    wrong_password = "cachorro_banana"
    result = authenticate_user(connection, existing_email, wrong_password)
    assert result is None

def test_authenticate_user_when_email_exists_and_password_is_correct():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email_user_1 = "test@example.com"
    existing_password_user_1 = "password123"
    register_user(connection, existing_email_user_1, existing_password_user_1)

    existing_email_user_2 = "test_222@example.com"
    existing_password_user_2 = "password456"
    register_user(connection, existing_email_user_2, existing_password_user_2)

    result = authenticate_user(connection, existing_email_user_2, existing_password_user_2)
    assert result == 2
    
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