import sqlite3
from typing import Any, Dict

from app.backend.commands import (get_any_random_musics,
                                  get_authenticated_user_id,
                                  get_music_recommendations_for_user,
                                  list_genres_for_user,
                                  list_musics_in_playlist,
                                  list_playlists_for_user,
                                  register_music_in_playlist,
                                  register_playlist, register_user,
                                  search_music)
from app.backend.database import start_users_database_connection
from app.backend.testing import start_sqlite_in_memory_database_connection


class Commands:
    """
    Simple wrapper around the commands module, to make it easier to test.
    That is: we can test the API more easily by mocking this class.
    """

    def __init__(self):
        pass

    def start_users_database_connection(self) -> sqlite3.Connection:
        return start_users_database_connection()

    def get_authenticated_user_id(self, connection: sqlite3.Connection, email: str, password: str) -> Dict[str, Any]:
        return get_authenticated_user_id(connection, email, password)

    def register_user(self, connection: sqlite3.Connection, email: str, password: str, name:str) -> Any:
        return register_user(connection, email, password, name)
    
    def register_playlist(self, connection: sqlite3.Connection, name: str, user_id: int) -> Any:
        return register_playlist(connection, name, user_id)
    
    def list_playlists_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return list_playlists_for_user(connection, user_id)
    
    def register_music_in_playlist(self, connection: sqlite3.Connection, playlist_id: int, music_id: int) -> Any:
        return register_music_in_playlist(connection, playlist_id, music_id)
    
    def list_musics_in_playlist(self, connection: sqlite3.Connection, playlist_id: int) -> Any:
        return list_musics_in_playlist(connection, playlist_id)
    
    def search_music(self, connection: sqlite3.Connection, search_term: str) -> Any:
        return search_music(connection, search_term)
    
    def get_music_recommendations_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return get_music_recommendations_for_user(connection, user_id)
    
    def get_any_random_musics(self, connection: sqlite3.Connection) -> Any:
        return get_any_random_musics(connection)
    
    def list_genres_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return list_genres_for_user(connection, user_id)

class MockedCommands(Commands):
    get_authenticated_user_id_response: Any
    register_user_response: Any
    list_genres_for_user_response: Any
    list_playlists_for_user_response: Any

    def __init__(self):
        self.register_music_in_playlist_called = False
        self.register_playlist_called = False

    def start_users_database_connection(self) -> sqlite3.Connection:
        return start_sqlite_in_memory_database_connection()

    def get_authenticated_user_id(self, connection: sqlite3.Connection, email: str, password: str) -> Dict[str, Any]:
        return self.get_authenticated_user_id_response

    def register_user(self, connection: sqlite3.Connection, email: str, password: str, name:str) -> Any:
        return self.register_user_response

    def register_playlist(self, connection: sqlite3.Connection, name: str, user_id: int) -> Any:
        self.register_playlist_called = True
        return None
    
    def register_music_in_playlist(self, connection: sqlite3.Connection, playlist_id: int, music_id: int) -> Any:
        self.register_music_in_playlist_called = True
        return None

    def list_musics_in_playlist(self, connection: sqlite3.Connection, playlist_id: int) -> Any:
        return None
    
    def search_music(self, connection: sqlite3.Connection, search_term: str) -> Any:
        return None
    
    def get_music_recommendations_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return None
    
    def get_any_random_musics(self, connection: sqlite3.Connection) -> Any:
        return None
    
    def list_genres_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return self.list_genres_for_user_response
    
    def list_playlists_for_user(self, connection: sqlite3.Connection, user_id: int) -> Any:
        return self.list_playlists_for_user_response
