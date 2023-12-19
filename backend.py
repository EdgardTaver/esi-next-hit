from flask import Flask
from app.backend.api import register_endpoints, API
from app.backend.factory import Commands

if __name__ == "__main__":
    app = Flask(__name__)

    cmd = Commands()
    api = API(cmd)
    register_endpoints(app, api)

    app.run(port=5000)
