from typing import Any, Dict, List, Optional

import requests

MUSIC_SEARCH_ENDPOINT = "http://127.0.0.1:5000/music/search"
LOGIN_ENDPOINT = "http://127.0.0.1:5000/user/login"
CHECK_LOGIN_ENDPOINT = "http://127.0.0.1:5000/user/is-logged"
REGISTER_ENDPOINT = "http://127.0.0.1:5000/user/register"
LOGOUT_ENDPOINT = "http://127.0.0.1:5000/user/logout"
CREATE_PLAYLIST_ENDPOINT = "http://127.0.0.1:5000/playlist/create"
LIST_PLAYLISTS_ENDPOINT = "http://127.0.0.1:5000/playlist/list"
SHOW_PLAYLIST_ENDPOINT = "http://127.0.0.1:5000/playlist/{playlist_id}/show"
ADD_MUSIC_TO_PLAYLIST_ENDPOINT = "http://127.0.0.1:5000/playlist/{playlist_id}/add-music"
MUSIC_RECOMMENDATIONS_ENDPOINT = "http://127.0.0.1:5000/music/recommendations"
RANDOM_MUSIC_RECOMMENDATIONS_ENDPOINT = "http://127.0.0.1:5000/music/random-recommendations"
USER_GENRES_ENDPOINT = "http://127.0.0.1:5000/user/music-genres"

def do_check_login():
    response = requests.get(CHECK_LOGIN_ENDPOINT)
    if response.status_code == 200:
        response_json = response.json()
        if response_json["is_logged"] == True:
            return True
    
    return False

def do_search(search_param: str) -> List[Any]:
    params = {"q": search_param}
    response = requests.get(MUSIC_SEARCH_ENDPOINT, params=params)

    if response.status_code != 200:
        return []

    return response.json()

def do_login(email: str, password: str) -> Optional[Dict[str, Any]]:
    payload = {"email": email, "password": password}
    response = requests.post(LOGIN_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return None
    
    return response.json()

def do_register(email: str, password: str, name: str) -> Optional[Dict[str, Any]]:
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return None
    
    return response.json()

def do_logout() -> bool:
    response = requests.get(LOGOUT_ENDPOINT)
    
    if response.status_code != 200:
        return False
    
    return True

def do_create_playlist(user_id: int, name: str) -> bool:
    payload = {"user_id": user_id, "playlist_name": name}
    response = requests.post(CREATE_PLAYLIST_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return False
    
    return True

def do_list_playlists(user_id: int) -> List[Any]:
    payload = {"user_id": user_id}
    response = requests.post(LIST_PLAYLISTS_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return []
    
    return response.json()

def do_show_playlist(playlist_id: int) -> List[Any]:
    response = requests.get(SHOW_PLAYLIST_ENDPOINT.format(playlist_id=playlist_id))
    
    if response.status_code != 200:
        return []
    
    return response.json()

def do_add_music_to_playlist(playlist_id: int, music_id: int) -> bool:
    payload = {"music_id": music_id}
    response = requests.post(ADD_MUSIC_TO_PLAYLIST_ENDPOINT.format(playlist_id=playlist_id), json=payload)
    
    if response.status_code != 200:
        return False
    
    return True

def do_get_music_recommendations_for_user(user_id: int) -> List[Any]:
    payload = {"user_id": user_id}
    response = requests.post(MUSIC_RECOMMENDATIONS_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return []
    
    return response.json()


def do_get_random_music_recommendations() -> List[Any]:
    response = requests.get(RANDOM_MUSIC_RECOMMENDATIONS_ENDPOINT)
    
    if response.status_code != 200:
        return []
    
    return response.json()

def do_get_user_genres(user_id: int) -> List[Any]:
    payload = {"user_id": user_id}
    response = requests.post(USER_GENRES_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return []
    
    return response.json()