from flask import Flask, request, jsonify, g

from app.infrastructure.database import create_users_table, register_user, get_authenticated_user_id, start_users_database_connection
from app.exceptions import EmailAlreadyRegisteredException
from flask import session

app = Flask(__name__)

@app.route('/login', methods=['POST']) # type:ignore
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    connection = start_users_database_connection()
    user_id = get_authenticated_user_id(connection, email, password)
    if user_id:
        session['user_id'] = user_id
        return jsonify({'message': 'Login successful', 'user_id': user_id})
    else:
        return jsonify({'message': 'Invalid email or password'})

@app.route('/register', methods=['POST']) # type:ignore
def register():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        connection = start_users_database_connection()
        register_user(connection, email, password)
        return jsonify({'message': 'User registered successfully'})
    
    except EmailAlreadyRegisteredException:
        return jsonify({'message': 'Email already registered'}), 400

@app.route('/playlist', methods=['POST']) # type:ignore
def create_playlist():
    user_id = session.get('user_id')

    
    if user_id:
        # Logic to create a new playlist for the logged in user
        return jsonify({'message': 'Playlist created successfully'})
    else:
        return jsonify({'message': 'User not logged in'}), 401




if __name__ == '__main__':
    app.run()
