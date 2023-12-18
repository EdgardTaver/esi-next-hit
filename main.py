from flask import Flask, jsonify, request, session, g

from app.exceptions import EmailAlreadyRegisteredException, MusicAlreadyInPlaylistException, MusicNotFoundException, PlaylistAlreadyExistsException, PlaylistNotFoundException
from app.infrastructure.commands import (get_authenticated_user_id,
                                         register_playlist, register_user, register_music_in_playlist)
from app.infrastructure.database import start_users_database_connection

app = Flask(__name__)
app.secret_key = "my-next-hit-secret"

@app.route('/login', methods=['POST']) # type:ignore
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    connection = start_users_database_connection()
    user_id = get_authenticated_user_id(connection, email, password)
    if user_id:
        session["USER_ID"] = user_id
        return jsonify({'message': 'Login successful', 'user_id': user_id})
    else:
        return jsonify({'message': 'Invalid email or password'})

@app.route('/logout', methods=['POST']) # type:ignore
def logout():
    session.pop("USER_ID", None)
    return jsonify({'message': 'Logout successful'})

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

@app.route('/playlist/create', methods=['POST']) # type:ignore
def create_playlist():
    user_id = session.get("USER_ID")

    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    connection = start_users_database_connection()
    try:
        playlist_name = request.json.get("playlist_name")
        register_playlist(connection, playlist_name, user_id)
        return jsonify({'message': 'Playlist created successfully'})
    
    except PlaylistAlreadyExistsException:
        return jsonify({'message': 'Playlist already exists'}), 400

    finally:
        connection.close()

@app.route('/playlist/add-music', methods=['POST']) # type:ignore
def add_music_to_playlist():
    user_id = session.get("USER_ID")

    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    connection = start_users_database_connection()
    try:
        playlist_id = request.json.get("playlist_id")
        music_id = request.json.get("music_id")
        register_music_in_playlist(connection, playlist_id, music_id)
        return jsonify({'message': 'Music added successfully to playlist'})
    
    except PlaylistNotFoundException:
        return jsonify({'message': 'Playlist does not exist'}), 400
    
    except MusicNotFoundException:
        return jsonify({'message': 'Music does not exist'}), 400
    
    except MusicAlreadyInPlaylistException:
        return jsonify({'message': 'Music already added to playlist'}), 400

    finally:
        connection.close()


if __name__ == '__main__':
    app.run()
