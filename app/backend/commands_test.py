
import pytest

from app.exceptions import (EmailAlreadyRegisteredException,
                            MusicAlreadyInPlaylistException,
                            MusicNotFoundException,
                            PlaylistAlreadyExistsException,
                            PlaylistNotFoundException)
from app.backend.commands import (get_authenticated_user_id,
                                         get_music_recommendations_for_user,
                                         list_genres_for_user,
                                         list_music_ids_for_user,
                                         list_musics_in_playlist,
                                         list_playlists_for_user,
                                         register_music_in_playlist,
                                         register_playlist, register_user,
                                         search_music)
from app.backend.database import (create_music_table,
                                         create_playlist_music_table,
                                         create_playlists_table,
                                         create_users_table, register_music)
from app.testing import start_sqlite_in_memory_database_connection


def test_register_user_when_email_is_new():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    new_email = "test@example.com"
    new_password = "password123"
    new_name = "Test User"
    exercise = register_user(connection, new_email, new_password, new_name)
    assert exercise == 1

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (new_email,))
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == new_name
    assert result[2] == new_email

    cursor.close()
    connection.close()

def test_register_user_when_email_already_exists():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    existing_name = "Test User"
    register_user(connection, existing_email, existing_password, existing_name)

    new_password = "password456"

    with pytest.raises(EmailAlreadyRegisteredException):
        register_user(connection, existing_email, new_password, existing_name)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (existing_email,))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()
    connection.close()

def test_get_authenticated_user_id_when_email_is_not_registered():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    existing_name = "Test User"
    register_user(connection, existing_email, existing_password, existing_name)

    non_existing_email = "cachorro@banana.com"
    any_password = "password456"

    result = get_authenticated_user_id(connection, non_existing_email, any_password)
    assert len(result) == 0

    connection.close()

def test_get_authenticated_user_id_when_email_exists_but_password_is_incorrect():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email = "test@example.com"
    existing_password = "password123"
    existing_name = "Test User"
    register_user(connection, existing_email, existing_password, existing_name)

    wrong_password = "cachorro_banana"
    result = get_authenticated_user_id(connection, existing_email, wrong_password)
    assert len(result) == 0

def test_get_authenticated_user_id_when_email_exists_and_password_is_correct():
    connection = start_sqlite_in_memory_database_connection()
    create_users_table(connection)

    existing_email_user_1 = "test@example.com"
    existing_password_user_1 = "password123"
    existing_name_1 = "Test User"
    user_id_1 = register_user(connection, existing_email_user_1, existing_password_user_1, existing_name_1)
    assert user_id_1 is not None

    existing_email_user_2 = "test_222@example.com"
    existing_password_user_2 = "password456"
    existing_name_2 = "Test User"
    user_id_2 = register_user(connection, existing_email_user_2, existing_password_user_2, existing_name_2)
    assert user_id_2 is not None

    result = get_authenticated_user_id(connection, existing_email_user_2, existing_password_user_2)
    assert result["user_id"] == user_id_2
    assert result["name"] == existing_name_2

    connection.close()


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
    connection.close()


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
    connection.close()


def test_register_music_in_playlist_when_playlist_not_found():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    invalid_playlist_id = 1
    existing_music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert existing_music_id is not None

    with pytest.raises(PlaylistNotFoundException):
        register_music_in_playlist(connection, invalid_playlist_id, existing_music_id)
    
    connection.close()


def test_register_music_in_playlist_when_music_not_found():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    existing_playlist_id = register_playlist(connection, "My Playlist", 1)
    assert existing_playlist_id is not None

    existing_music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert existing_music_id is not None

    invalid_music_id = existing_music_id + 1

    with pytest.raises(MusicNotFoundException):
        register_music_in_playlist(connection, existing_playlist_id, invalid_music_id)
    
    connection.close()


def test_register_music_in_playlist_when_music_not_in_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    playlist_id = register_playlist(connection, "My Playlist", 1)
    assert playlist_id is not None

    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM playlist_music WHERE playlist_id=? AND music_id=?", (playlist_id, music_id))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == playlist_id
    assert result[1] == music_id

    cursor.close()
    connection.close()


def test_register_music_in_playlist_when_music_already_in_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    playlist_id = register_playlist(connection, "My Playlist", 1)
    assert playlist_id is not None
    
    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    with pytest.raises(MusicAlreadyInPlaylistException):
        register_music_in_playlist(connection, playlist_id, music_id)

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM playlist_music WHERE playlist_id=? AND music_id=?", (playlist_id, music_id))
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()
    connection.close()

def test_list_playlists_for_user_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    user_id = 1

    playlist_id = register_playlist(connection, "My Playlist", user_id)
    assert playlist_id is not None
    
    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    result = list_playlists_for_user(connection, user_id)
    assert len(result) == 1
    assert result[0]["id"] == playlist_id
    assert result[0]["name"] == "My Playlist"
    assert result[0]["user_id"] == user_id
    
    connection.close()


def test_list_playlists_for_user_no_playlists_found():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    existing_user_id = 1

    playlist_id = register_playlist(connection, "My Playlist", existing_user_id)
    assert playlist_id is not None
    
    music_id = register_music(connection, "music 1", "artist 1", "genre 1", "any.url")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    non_existing_user_id = 2

    result = list_playlists_for_user(connection, non_existing_user_id)
    assert len(result) == 0
    
    connection.close()


def test_list_musics_in_playlist_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    any_user_id = 1
    playlist_id = register_playlist(connection, "My Playlist", any_user_id)
    assert playlist_id is not None
    
    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None
    
    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    register_music_in_playlist(connection, playlist_id, music_id_1)
    register_music_in_playlist(connection, playlist_id, music_id_2)

    result = list_musics_in_playlist(connection, playlist_id)
    assert len(result) == 2
    assert result[0]["id"] == music_id_1
    assert result[0]["title"] == "Sorry"
    assert result[0]["artist"] == "Justin Bieber"
    assert result[0]["genre"] == "norwegian black metal"
    assert result[0]["image_url"] == "url/image_1"

    assert result[1]["id"] == music_id_2
    assert result[1]["title"] == "Calabasas"
    assert result[1]["artist"] == "Tritonal"
    assert result[1]["genre"] == "electronic music"
    assert result[1]["image_url"] == "url/image_2"
    
    connection.close()

def test_list_musics_in_playlist_empty_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    any_user_id = 1
    playlist_id = register_playlist(connection, "My Playlist", any_user_id)
    assert playlist_id is not None

    result = list_musics_in_playlist(connection, playlist_id)
    assert len(result) == 0
    
    connection.close()

def test_list_musics_in_playlist_non_existent_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    any_user_id = 1
    playlist_id = register_playlist(connection, "My Playlist", any_user_id)
    assert playlist_id is not None

    music_id = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    non_existent_playlist_id = playlist_id + 1

    result = list_musics_in_playlist(connection, non_existent_playlist_id)
    assert len(result) == 0
    
    connection.close()


def test_search_music_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_music_table(connection)

    register_music(connection, "Stop the music!", "The Dogs", "nu disco", "url/image_1")
    register_music(connection, "Stop the music!", "Ariana Grande", "new age", "url/image_2")
    register_music(connection, "Don't Stop the music!", "The Bananas", "death metal", "url/image_3")

    results = search_music(connection, "music")

    assert len(results) == 3
    assert results[0]["title"] == "Don't Stop the music!"
    assert results[0]["artist"] == "The Bananas"
    assert results[0]["genre"] == "death metal"
    assert results[0]["image_url"] == "url/image_3"

    assert results[1]["title"] == "Stop the music!"
    assert results[1]["artist"] == "The Dogs"
    assert results[1]["genre"] == "nu disco"
    assert results[1]["image_url"] == "url/image_1"

    assert results[2]["title"] == "Stop the music!"
    assert results[2]["artist"] == "Ariana Grande"
    assert results[2]["genre"] == "new age"
    assert results[2]["image_url"] == "url/image_2"
    
    # should be ordered by title and id


def test_search_music_no_entries_found():
    connection = start_sqlite_in_memory_database_connection()
    create_music_table(connection)

    register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_1")

    results = search_music(connection, "bohemian")
    assert len(results) == 0


def test_search_music_case_insensitivity():
    connection = start_sqlite_in_memory_database_connection()
    create_music_table(connection)

    register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    register_music(connection, "SORRY", "Justin Bieber", "norwegian black metal", "url/image_1")
    register_music(connection, "sorry", "Justin Bieber", "norwegian black metal", "url/image_1")

    results = search_music(connection, "sOrRy")
    assert len(results) == 3
    assert results[0]["title"] == "Sorry"
    assert results[1]["title"] == "SORRY"
    assert results[2]["title"] == "sorry"

def test_list_genres_for_user_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    user_id = 1
    
    playlist_id_1 = register_playlist(connection, "Dogs 1", user_id)
    assert playlist_id_1 is not None

    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None

    register_music_in_playlist(connection, playlist_id_1, music_id_1)

    playlist_id_2 = register_playlist(connection, "Banana 2", user_id)
    assert playlist_id_2 is not None

    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    register_music_in_playlist(connection, playlist_id_2, music_id_2)

    result = list_genres_for_user(connection, user_id)
    assert result == ["electronic music", "norwegian black metal"]

    connection.close()

def test_list_genres_for_user_different_users():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    user_id_1 = 1
    
    playlist_id_1 = register_playlist(connection, "Dogs 1", user_id_1)
    assert playlist_id_1 is not None

    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None

    register_music_in_playlist(connection, playlist_id_1, music_id_1)

    user_id_2 = 2

    playlist_id_2 = register_playlist(connection, "Banana 2", user_id_2)
    assert playlist_id_2 is not None

    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    register_music_in_playlist(connection, playlist_id_2, music_id_2)

    result = list_genres_for_user(connection, user_id_1)
    assert result == ["norwegian black metal"]

    connection.close()

def test_list_genres_for_user_no_musics_for_user():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    existing_user_id = 1
    
    playlist_id = register_playlist(connection, "Dogs 1", existing_user_id)
    assert playlist_id is not None

    music_id = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    non_existing_user_id = 2

    result = list_genres_for_user(connection, non_existing_user_id)
    assert len(result) == 0

    connection.close()

def test_list_music_ids_for_user_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)
    
    user_id = 1
    
    playlist_id_1 = register_playlist(connection, "Dogs 1", user_id)
    assert playlist_id_1 is not None

    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None

    register_music_in_playlist(connection, playlist_id_1, music_id_1)

    playlist_id_2 = register_playlist(connection, "Banana 2", user_id)
    assert playlist_id_2 is not None

    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    register_music_in_playlist(connection, playlist_id_2, music_id_2)

    result = list_music_ids_for_user(connection, user_id)
    assert result == [music_id_1, music_id_2]

    connection.close()

def test_list_music_ids_for_user_different_users():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)
    
    user_id_1 = 1
    
    playlist_id_1 = register_playlist(connection, "Dogs 1", user_id_1)
    assert playlist_id_1 is not None

    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None

    register_music_in_playlist(connection, playlist_id_1, music_id_1)

    user_id_2 = 2

    playlist_id_2 = register_playlist(connection, "Banana 2", user_id_2)
    assert playlist_id_2 is not None

    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    register_music_in_playlist(connection, playlist_id_2, music_id_2)

    result = list_music_ids_for_user(connection, user_id_1)
    assert result == [music_id_1]

    connection.close()

def test_list_music_ids_for_user_no_musics_for_user():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)
    
    existing_user_id = 1
    
    playlist_id = register_playlist(connection, "Dogs 1", existing_user_id)
    assert playlist_id is not None

    music_id = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id is not None

    register_music_in_playlist(connection, playlist_id, music_id)

    non_existing_user_id = 2

    result = list_music_ids_for_user(connection, non_existing_user_id)
    assert len(result) == 0

    connection.close()

def test_get_music_recommendations_for_user_regular_scenario():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)
    
    music_id_1 = register_music(connection, "Sorry", "Justin Bieber", "norwegian black metal", "url/image_1")
    assert music_id_1 is not None

    music_id_2 = register_music(connection, "Calabasas", "Tritonal", "electronic music", "url/image_2")
    assert music_id_2 is not None

    music_id_3 = register_music(connection, "Stop the music!", "The Dogs", "electronic music", "url/image_3")
    assert music_id_3 is not None

    music_id_4 = register_music(connection, "Seven Nation Army", "The White Stripes", "norwegian black metal", "url/image_4")
    assert music_id_4 is not None

    music_id_5 = register_music(connection, "Numb", "Linkin Park", "nu metal", "url/image_5")
    assert music_id_5 is not None
    
    user_id = 1
    
    playlist_id_1 = register_playlist(connection, "Angry Mode", user_id)
    assert playlist_id_1 is not None
    register_music_in_playlist(connection, playlist_id_1, music_id_1)

    playlist_id_2 = register_playlist(connection, "Party Mode", user_id)
    assert playlist_id_2 is not None
    register_music_in_playlist(connection, playlist_id_2, music_id_2)


    result = get_music_recommendations_for_user(connection, user_id)
    assert len(result) == 2

    assert result[0]["id"] == music_id_3 or result[0]["id"] == music_id_4
    assert result[1]["id"] == music_id_3 or result[1]["id"] == music_id_4
    # music id 5 contains a genre that is not in any playlist of the user
    # musics already in playlist should not be returned

    connection.close()

def test_get_music_recommendations_for_user_when_user_has_no_playlist():
    connection = start_sqlite_in_memory_database_connection()
    create_playlists_table(connection)
    create_music_table(connection)
    create_playlist_music_table(connection)

    music_id_1 = register_music(connection, "Stop the music!", "The Dogs", "electronic music", "url/image_3")
    assert music_id_1 is not None

    music_id_2 = register_music(connection, "Seven Nation Army", "The White Stripes", "norwegian black metal", "url/image_4")
    assert music_id_2 is not None

    music_id_3 = register_music(connection, "Numb", "Linkin Park", "nu metal", "url/image_5")
    assert music_id_3 is not None
    
    user_id = 1

    result = get_music_recommendations_for_user(connection, user_id)
    assert len(result) == 3

    sorted_result_music_ids = sorted([result[0]["id"], result[1]["id"], result[2]["id"]])
    assert sorted_result_music_ids == [music_id_1, music_id_2, music_id_3]
    # user has no know tastes, any music can be recommended
    # the sorting is to ensure the test is deterministic

    connection.close()