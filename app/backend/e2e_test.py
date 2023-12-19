import os
from flask import Flask
from app.backend.api import API
from app.backend.config import TEST_DATABASE_FILE

from app.backend.factory import E2ETestCommands
from app.backend.api import register_endpoints
from app.backend.database import database_setup, register_music


def test_regular_user_flow():
    app = Flask(__name__)
    cmd = E2ETestCommands()
    api = API(cmd)
    register_endpoints(app, api)
    database_setup(cmd.start_users_database_connection())
    music_id = register_music(cmd.start_users_database_connection(), "Sorry", "Justin Bieber", "folk music", "any.url")
    assert music_id is not None

    try:
        # Register a user
        response = app.test_client().post("/user/register", json={
            "email": "bon@jovi.com",
            "password": "123456",
            "name": "Bon Jovi",
        })
        assert response.status_code == 200
        assert response.json is not None
        user_id = response.json["user_id"]

        # Fails to login with wrong password
        response = app.test_client().post("/user/login", json={
            "email": "bon@jovi.com",
            "password": "wrong_pass",
        })
        assert response.status_code == 401

        # Login as that user
        response = app.test_client().post("/user/login", json={
            "email": "bon@jovi.com",
            "password": "123456",
        })
        assert response.status_code == 200

        # Create a playlist
        response = app.test_client().post("/playlist/create", json={
            "user_id": user_id,
            "playlist_name": "Not a bad playlist",
        })
        assert response.status_code == 200
        playlist_id = 1

        # Add music to playlist
        response = app.test_client().post(f"/playlist/{playlist_id}/add-music", json={
            "music_id": music_id,
        })
        assert response.status_code == 200

        # List musics in playlist
        response = app.test_client().get(f"/playlist/{playlist_id}/show")
        assert response.status_code == 200
    
    finally:
        os.unlink(TEST_DATABASE_FILE)
