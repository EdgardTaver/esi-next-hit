from flask import Flask
from app.infrastructure.api import register_endpoints

if __name__ == "__main__":
    app = Flask(__name__)
    register_endpoints(app)

    app.run(debug=True, port=5000)
