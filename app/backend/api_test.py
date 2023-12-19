from flask import Flask

from app.backend.api import register_endpoints


def test_endpoint_login():
    app = Flask(__name__)
    register_endpoints(app)
    
    response = app.test_client().post("/user/login", json={
        "email": "cachorro@banana.com",
        "password": "123456"
    })

    assert response.status_code == 200