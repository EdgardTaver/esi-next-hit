from flask import Flask

from app.backend.api import API, register_endpoints
from app.backend.factory import MockedCommands
from app.backend.database import database_setup


def test_endpoint_login_missing_email():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/login", json={
        "password": "123456",
    })

    assert response.status_code == 400

def test_endpoint_login_missing_password():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/login", json={
        "email": "cachorro@banana.com",
    })

    assert response.status_code == 400

def test_endpoint_login_invalid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.get_authenticated_user_id_response = {}
    
    response = app.test_client().post("/user/login", json={
        "email": "cachorro@banana.com",
        "password": "123456",
    })

    assert response.status_code == 401

def test_endpoint_login_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.get_authenticated_user_id_response = {
        "user_id": 1,
        "name": "Cachorro Banana",
    }
    
    response = app.test_client().post("/user/login", json={
        "email": "cachorro@banana.com",
        "password": "123456",
    })

    assert response.status_code == 200

def test_endpoint_register_missing_email():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/register", json={
        "password": "123456",
        "name": "Cachorro Banana",
    })

    assert response.status_code == 400

def test_endpoint_register_missing_password():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/register", json={
        "email": "cachorro@banana.com",
        "name": "Cachorro Banana",
    })

    assert response.status_code == 400

def test_endpoint_register_missing_name():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/register", json={
        "email": "cachorro@banana.com",
        "password": "123456",
    })

    assert response.status_code == 400


def test_endpoint_register_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.register_user_response = 1
    
    response = app.test_client().post("/user/register", json={
        "email": "cachorro@banana.com",
        "password": "123456",
        "name": "Cachorro Banana",
    })

    assert response.status_code == 200
    assert response.json is not None
    assert response.json["user_id"] == 1
    assert response.json["name"] == "Cachorro Banana"

def test_endpoint_get_user_music_genres_missing_user_id():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/user/music-genres", json={
    })

    assert response.status_code == 400

def test_endpoint_get_user_music_genres_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.list_genres_for_user_response = ["pop"]
    
    response = app.test_client().post("/user/music-genres", json={
        "user_id": 1,
    })

    assert response.status_code == 200
    assert response.json is not None
    assert response.json == ["pop"]

def test_endpoint_create_playlist_missing_name():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/playlist/create", json={
        "user_id": 1,
    })

    assert response.status_code == 400

def test_endpoint_create_playlist_missing_user_id():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/playlist/create", json={
        "playlist_name": "Cachorro Banana",
    })

    assert response.status_code == 400

def test_endpoint_create_playlist_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/playlist/create", json={
        "playlist_name": "Cachorro Banana",
        "user_id": 1,
    })

    assert response.status_code == 200
    assert cmd.register_playlist_called

def test_endpoint_list_playlists_missing_user_id():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)
    
    response = app.test_client().post("/playlist/list", json={
    })

    assert response.status_code == 400

def test_endpoint_list_playlists_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.list_playlists_for_user_response = [{"name": "Melhores do Ano"}]

    response = app.test_client().post("/playlist/list", json={
        "user_id": 1,
    })

    assert response.status_code == 200
    assert response.json is not None
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Melhores do Ano"

def test_endpoint_add_music_to_playlist_missing_music_id():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    playlist_id = 1
    response = app.test_client().post(f"/playlist/{playlist_id}/add-music", json={
    })

    assert response.status_code == 400

def test_endpoint_add_music_to_playlist_valid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    playlist_id = 1
    response = app.test_client().post(f"/playlist/{playlist_id}/add-music", json={
        "music_id": 1,
    })

    assert response.status_code == 200
    assert cmd.register_music_in_playlist_called

def test_endpoint_show_playlist():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.list_musics_in_playlist_response = [{"name": "Cachorro Banana"}]

    playlist_id = 1
    response = app.test_client().get(f"/playlist/{playlist_id}/show")

    assert response.status_code == 200
    assert response.json is not None
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Cachorro Banana"