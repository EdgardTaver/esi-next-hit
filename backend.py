from flask import Flask
from app.backend.api import register_endpoints

if __name__ == "__main__":
    app = Flask(__name__)
    register_endpoints(app)

    app.run(port=5000)
