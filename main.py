import sqlite3
from flask import Flask, request, jsonify, g

from app.infrastructure.database import create_users_table, register_user, authenticate_user, start_users_database_connection
from app.exceptions import EmailAlreadyRegisteredException

app = Flask(__name__)

@app.route('/login', methods=['POST']) #type:ignore
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if authenticate_user(g.users_database_connection, email, password):
        g.logged_in = True
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid email or password'})

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        register_user(g.users_database_connection, email, password)
        return jsonify({'message': 'User registered successfully'})
    
    except EmailAlreadyRegisteredException:
        return jsonify({'message': 'Email already registered'}), 400


@app.route('/protected', methods=['GET'])
def protected():
    if not getattr(g, 'logged_in', False):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': 'Protected endpoint'})

if __name__ == '__main__':
    connection = start_users_database_connection()
    g.users_database_connection = connection
    
    create_users_table(g.users_database_connection)

    app.run()

