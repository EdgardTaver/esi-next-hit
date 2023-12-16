import hashlib
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)

def encrypt_password(password: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def authenticate_user(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result is not None:
        stored_password = result[0]
        if encrypt_password(password) == stored_password:
            return True

    return False

@app.route('/login', methods=['POST']) #type:ignore
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if authenticate_user(username, password):
        g.logged_in = True
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'})

@app.route('/protected', methods=['GET'])
def protected():
    if not getattr(g, 'logged_in', False):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': 'Protected endpoint'})

if __name__ == '__main__':
    app.run()

