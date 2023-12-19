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

def test_endpoint_register_invalid_response():
    app = Flask(__name__)
    cmd = MockedCommands()
    api = API(cmd)
    register_endpoints(app, api)

    cmd.register_user_response = None
    
    response = app.test_client().post("/user/register", json={
        "email": "cachorro@banana.com",
        "password": "123456",
        "name": "Cachorro Banana",
    })

    assert response.status_code == 500


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