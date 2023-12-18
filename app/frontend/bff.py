import requests
from typing import Any, List, Optional

MUSIC_SEARCH_ENDPOINT = "http://127.0.0.1:5000/music/search"
LOGIN_ENDPOINT = "http://127.0.0.1:5000/user/login"
CHECK_LOGIN_ENDPOINT = "http://127.0.0.1:5000/user/is-logged"
REGISTER_ENDPOINT = "http://127.0.0.1:5000/user/register"
LOGOUT_ENDPOINT = "http://127.0.0.1:5000/user/logout"

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

def do_login(email: str, password: str) -> Optional[int]:
    payload = {"email": email, "password": password}
    response = requests.post(LOGIN_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return None
    
    return response.json()["user_id"]

def do_register(email: str, password: str) -> Optional[int]:
    payload = {"email": email, "password": password}
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return None
    
    return response.json()["user_id"]

def do_logout() -> bool:
    response = requests.get(LOGOUT_ENDPOINT)
    
    if response.status_code != 200:
        return False
    
    return True

