from flask import Flask, g, jsonify, request, session

from app.exceptions import (EmailAlreadyRegisteredException,
                            MusicAlreadyInPlaylistException,
                            MusicNotFoundException,
                            PlaylistAlreadyExistsException,
                            PlaylistNotFoundException)
from app.infrastructure.commands import (get_authenticated_user_id,
                                         list_musics_in_playlist,
                                         list_playlists_for_user,
                                         register_music_in_playlist,
                                         register_playlist, register_user,
                                         search_music)
from app.infrastructure.database import start_users_database_connection

app = Flask(__name__)
app.secret_key = "my-next-hit-secret"

@app.route("/user/login", methods=['POST']) # type:ignore
def endpoint_login():
    email = request.json.get("email")
    password = request.json.get("password")

    connection = start_users_database_connection()
    user_id = get_authenticated_user_id(connection, email, password)
    connection.close()
    
    if user_id:
        session["USER_ID"] = user_id
        return jsonify({'message': 'Login successful', 'user_id': user_id})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route("/user/is-logged", methods=["GET"]) # type:ignore
# TODO: this method is not necessary
def endpoint_is_logged():
    user_id = session.get("USER_ID")

    if user_id:
        return jsonify({'is_logged': True})
    
    else:
        return jsonify({'is_logged': False})


@app.route("/user/logout", methods=["GET"]) # type:ignore
# TODO: this method is not necessary
def endpoint_logout():
    session.pop("USER_ID", None)
    return jsonify({'message': 'Logout successful'})

@app.route("/user/register", methods=['POST']) # type:ignore
def endpoint_register():
    email = request.json.get("email")
    password = request.json.get("password")

    connection = start_users_database_connection()
    try:
        user_id = register_user(connection, email, password)
        return jsonify({'message': 'User registered successfully', 'user_id': user_id})
    
    except EmailAlreadyRegisteredException:
        return jsonify({'message': 'Email already registered'}), 400
    
    finally:
        connection.close()

@app.route("/playlist/create", methods=['POST']) # type:ignore
def endpoint_create_playlist():
    connection = start_users_database_connection()
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400
        
        playlist_name = request.json.get("playlist_name")
        if not playlist_name:
            return jsonify({'message': 'Missing playlist_name'}), 400
        # TODO: test this

        register_playlist(connection, playlist_name, user_id)
        return jsonify({'message': 'Playlist created successfully'})
    
    except PlaylistAlreadyExistsException:
        return jsonify({'message': 'Playlist already exists'}), 400

    finally:
        connection.close()

@app.route("/playlist/list", methods=['POST']) # type:ignore
def endpoint_list_playlists():
    connection = start_users_database_connection()
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400

        playlists = list_playlists_for_user(connection, user_id)
        return jsonify(playlists)
    
    except Exception:
        return jsonify({'message': 'Unexpected issue'}), 500

    finally:
        connection.close()

@app.route("/playlist/add-music", methods=['POST']) # type:ignore
def endpoint_add_music_to_playlist():
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

@app.route("/playlist/<playlist_id>/show", methods=['GET']) # type:ignore
def endpoint_show_playlist(playlist_id: int):
    connection = start_users_database_connection()
    try:
        if not playlist_id:
            return jsonify({'message': 'Missing playlist id'}), 400

        musics = list_musics_in_playlist(connection, playlist_id)
        return jsonify(musics)
    
    except Exception:
        return jsonify({'message': 'Unexpected issue'}), 500

    finally:
        connection.close()

@app.route("/music/search", methods=['GET']) # type:ignore
def endpoint_search_music():
    search_term = request.args.get("q")
    if search_term is None:
        return jsonify({'message': 'Missing search term'}), 400

    connection = start_users_database_connection()
    try:
        results = search_music(connection, search_term)
        return results
    
    except Exception:
        return jsonify({'message': 'Unexpected issue'}), 500

    finally:
        connection.close()

if __name__ == '__main__':
    app.run()
