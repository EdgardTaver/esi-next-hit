from flask import Flask, request, jsonify, g

from app.infrastructure.database import create_users_table, register_user, authenticate_user, start_users_database_connection
from app.exceptions import EmailAlreadyRegisteredException

app = Flask(__name__)

@app.route('/login', methods=['POST']) # type:ignore
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    connection = start_users_database_connection()
    if authenticate_user(connection, email, password):
        g.logged_in = True
        return jsonify({'message': 'Login successful'})
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


@app.route('/protected', methods=['GET']) # type:ignore
def protected():
    if not getattr(g, 'logged_in', False):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({'message': 'Protected endpoint'})


if __name__ == '__main__':
    with app.app_context():
        connection = start_users_database_connection()
        create_users_table(connection)

    app.run()
