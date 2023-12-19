from flask import Flask, jsonify, request

from app.backend.exceptions import (EmailAlreadyRegisteredException,
                            MusicAlreadyInPlaylistException,
                            MusicNotFoundException,
                            PlaylistAlreadyExistsException,
                            PlaylistNotFoundException)

from app.backend.factory import Commands

class API:
    def __init__(self, cmd: Commands) -> None:
        self.cmd = cmd

    def endpoint_login(self):
        email = request.json.get("email")
        if not email:
            return jsonify({'message': 'Missing email'}), 400
        
        password = request.json.get("password")
        if not password:
            return jsonify({'message': 'Missing password'}), 400

        connection = self.cmd.start_users_database_connection()
        try:
            result = self.cmd.get_authenticated_user_id(connection, email, password)    
            if len(result) > 0:
                return jsonify({
                    "message": "Login successful",
                    "user_id": result["user_id"],
                    "name": result["name"]})
            else:
                return jsonify({'message': 'Invalid email or password'}), 401
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()


    def endpoint_register(self):
        email = request.json.get("email")
        if not email:
            return jsonify({'message': 'Missing email'}), 400

        password = request.json.get("password")
        if not password:
            return jsonify({'message': 'Missing password'}), 400
        
        name = request.json.get("name")
        if not name:
            return jsonify({'message': 'Missing name'}), 400

        connection = self.cmd.start_users_database_connection()
        try:
            user_id = self.cmd.register_user(connection, email, password, name)
            return jsonify({'message': 'User registered successfully', 'user_id': user_id, 'name': name})
        
        except EmailAlreadyRegisteredException:
            return jsonify({'message': 'Email already registered'}), 400
        
        finally:
            connection.close()

    def endpoint_get_user_music_genres(self):
        connection = self.cmd.start_users_database_connection()
        try:
            user_id = request.json.get("user_id")
            if not user_id:
                return jsonify({'message': 'Missing user_id'}), 400
            
            result = self.cmd.list_genres_for_user(connection, user_id)
            return jsonify(result)
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500
        
        finally:
            connection.close()

    def endpoint_create_playlist(self):
        connection = self.cmd.start_users_database_connection()
        try:
            user_id = request.json.get("user_id")
            if not user_id:
                return jsonify({'message': 'Missing user_id'}), 400
            
            playlist_name = request.json.get("playlist_name")
            if not playlist_name:
                return jsonify({'message': 'Missing playlist_name'}), 400

            self.cmd.register_playlist(connection, playlist_name, user_id)
            return jsonify({'message': 'Playlist created successfully'})
        
        except PlaylistAlreadyExistsException:
            return jsonify({'message': 'Playlist already exists'}), 400

        finally:
            connection.close()

    def endpoint_list_playlists(self):
        connection = self.cmd.start_users_database_connection()
        try:
            user_id = request.json.get("user_id")
            if not user_id:
                return jsonify({'message': 'Missing user_id'}), 400

            playlists = self.cmd.list_playlists_for_user(connection, user_id)
            return jsonify(playlists)
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()

    def endpoint_add_music_to_playlist(self, cmd: Commands):
        connection = self.cmd.start_users_database_connection()
        try:
            playlist_id = request.json.get("playlist_id")
            if not playlist_id:
                return jsonify({'message': 'Missing playlist id'}), 400
            
            music_id = request.json.get("music_id")
            if not music_id:
                return jsonify({'message': 'Missing music_id'}), 400
            
            self.cmd.register_music_in_playlist(connection, playlist_id, music_id)
            return jsonify({'message': 'Music added successfully to playlist'})
        
        except PlaylistNotFoundException:
            return jsonify({'message': 'Playlist does not exist'}), 400
        
        except MusicNotFoundException:
            return jsonify({'message': 'Music does not exist'}), 400
        
        except MusicAlreadyInPlaylistException:
            return jsonify({'message': 'Music already added to playlist'}), 400

        finally:
            connection.close()

    def endpoint_show_playlist(self):
        connection = self.cmd.start_users_database_connection()
        try:
            playlist_id = request.json.get("playlist_id")
            if not playlist_id:
                return jsonify({'message': 'Missing playlist id'}), 400

            musics = self.cmd.list_musics_in_playlist(connection, playlist_id)
            return jsonify(musics)
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()

    def endpoint_search_music(self):
        search_term = request.args.get("q")
        if search_term is None:
            return jsonify({'message': 'Missing search term'}), 400

        connection = self.cmd.start_users_database_connection()
        try:
            results = self.cmd.search_music(connection, search_term)
            return results
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()

    def endpoint_get_music_recommendations(self):
        connection = self.cmd.start_users_database_connection()
        try:
            user_id = request.json.get("user_id")
            if not user_id:
                return jsonify({'message': 'Missing user_id'}), 400
            
            results = self.cmd.get_music_recommendations_for_user(connection, user_id)
            return results
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()

    def endpoint_get_music_random_recommendations(self):
        connection = self.cmd.start_users_database_connection()
        try:
            results = self.cmd.get_any_random_musics(connection)
            return results
        
        except Exception:
            return jsonify({'message': 'Unexpected issue'}), 500

        finally:
            connection.close()

def register_endpoints(app: Flask, api: API):
    app.add_url_rule("/user/login", view_func=api.endpoint_login, methods=['POST'])
    app.add_url_rule("/user/register", view_func=api.endpoint_register, methods=['POST'])
    app.add_url_rule("/user/music-genres", view_func=api.endpoint_get_user_music_genres, methods=["POST"])
    app.add_url_rule("/playlist/create", view_func=api.endpoint_create_playlist, methods=['POST'])
    app.add_url_rule("/playlist/list", view_func=api.endpoint_list_playlists, methods=['POST'])
    app.add_url_rule("/playlist/<playlist_id>/add-music", view_func=api.endpoint_add_music_to_playlist, methods=['POST'])
    app.add_url_rule("/playlist/<playlist_id>/show", view_func=api.endpoint_show_playlist, methods=['GET'])
    app.add_url_rule("/music/search", view_func=api.endpoint_search_music, methods=['GET'])
    app.add_url_rule("/music/recommendations", view_func=api.endpoint_get_music_recommendations, methods=['POST'])
    app.add_url_rule("/music/random-recommendations", view_func=api.endpoint_get_music_random_recommendations, methods=['GET'])