import hashlib
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)

def encrypt_password(password: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def authenticate_user(email: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        stored_password = result[0]
        if encrypt_password(password) == stored_password:
            return True

    return False

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)")
    conn.commit()

def initialize_database():
    create_users_table()

@app.route('/login', methods=['POST']) #type:ignore
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if authenticate_user(email, password):
        g.logged_in = True
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid email or password'})

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get("email")
    password = request.json.get("password")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is not None:
        return jsonify({'message': 'Email already exists'})

    hashed_password = encrypt_password(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
    conn.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/protected', methods=['GET'])
def protected():
    if not getattr(g, 'logged_in', False):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': 'Protected endpoint'})

if __name__ == '__main__':
    initialize_database()
    app.run()

@app.route('/protected', methods=['GET'])
def protected():
    if not getattr(g, 'logged_in', False):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': 'Protected endpoint'})

if __name__ == '__main__':
    app.run()

