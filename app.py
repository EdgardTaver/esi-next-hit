## pip install streamlit
## pip install streamlit_option_menu
## pip install streamlit_searchbox

## python -m streamlit run app.py

"""
TODOs:

- [ ] Find a new package for this
- [ ] Derive configs from app.config file
"""

from typing import Any, List, Optional
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_searchbox import st_searchbox
import requests

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

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "should_display_login_success" not in st.session_state:
    st.session_state["should_display_login_success"] = False

if "should_display_logout_message" not in st.session_state:
    st.session_state["should_display_logout_message"] = False

st.set_page_config(page_title="NextHit", page_icon=":musical_note:", layout="centered")

st.title(":musical_note: NextHit")
st.write("Encontre sua próxima música favorita")

selected = option_menu(
    menu_title="Menu",
    menu_icon="music-note-beamed",
    options=["Descobrir", "Playlists", "Perfil"],
    icons=["globe", "music-note-list", "person"],
    orientation="horizontal",
)

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

def do_register(email: str, password: str) -> bool:
    payload = {"email": email, "password": password}
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    
    if response.status_code != 200:
        return False
    
    return True

def do_logout() -> bool:
    response = requests.get(LOGOUT_ENDPOINT)
    
    if response.status_code != 200:
        return False
    
    return True


if selected=="Descobrir":
    title = st.text_input("Procure por uma música...", "")
    if title:
        results = do_search(title)
        if len(results) == 0:
            st.error("Nenhuma música encontrada")
        
        else:
            for music in results:
                col1, col2 = st.columns((1,2.75))
                col1.image(music["image_url"], width=150)
                col2.subheader(music["title"])
                col2.write(music["artist"])
                col2.write(f"Gênero: {music['genre']}")
                col2.button(key=music["id"], label="Adicionar à playlist")

    st.subheader("Descoberta diária")
    st.image(["playlist.jpg", "playlist.jpg", "playlist.jpg"], caption=["Playlist Diária", "Descubra: MPB", "Descubra: Rock"], width=150)
    st.subheader("Músicas recomendadas")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150)
    st.subheader("Pop")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150)
    st.subheader("Eletrônica")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150) 

if selected=="Playlists":
    st_searchbox(search_function="List", placeholder="Procure por um gênero")
    st.subheader("Playlists dos seus gêneros favoritos")
    st.image(["playlist.jpg", "playlist.jpg", "playlist.jpg", "playlist.jpg"], caption=["Pop", "Eletrônica", "Rock", "Jazz"], width=150)
    st.subheader("Playlists salvas")
    st.image(["playlist.jpg", "playlist.jpg", "playlist.jpg", "playlist.jpg"], caption=["Mix melhores", "Chiclete", "Relaxando", "Focado"], width=150)

if selected=="Perfil":
    if st.session_state["should_display_login_success"]:
        st.success("Login realizado com sucesso!")
        st.session_state["should_display_login_success"] = False
    
    if st.session_state["should_display_logout_message"]:
        st.warning("Logout realizado com sucesso. Até breve!")
        st.session_state["should_display_logout_message"] = False
    
    if st.session_state["user_id"] is not None :
        
        st.write("Olá!")
        # TODO: add more info
        logout = st.button(key="logout", label="Logout")
        if logout:
            response = do_logout()
            if not response:
                st.error("Erro ao fazer logout")
            else:
                st.session_state["user_id"] = None
                st.session_state["should_display_logout_message"] = True
    
    else:
        with st.form(key="login_form"):
            st.subheader("Faça login para acessar seu perfil")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login")
            if submitted:
                login_response = do_login(email, password)
                if not login_response:
                    st.error("E-mail ou senha inválidos.")
                else:
                    st.session_state["user_id"] = login_response
                    st.session_state["should_display_login_success"] = True
        
        # with st.form(key="register_form"):
        #     st.subheader("Não possui uma conta? Cadastre-se!")

        #     email = st.text_input("Email")
        #     password = st.text_input("Password", type="password")

        #     submitted = st.form_submit_button("Cadastrar")
        #     if submitted:
        #         register_response = do_register(email, password)
        #         if not register_response:
        #             st.error("E-mail já cadastrado.")
        #         else:
        #             st.session_state["is_logged"] = True
        #             st.session_state["should_display_login_success"] = True

    # st.subheader("Nome do Perfil")
    # st.image("axolote.jpg", width=100)
    # left_column, right_column = st.columns(2)
    # with left_column:
    #     st.subheader("Minhas playlists")
    # with right_column:
    #     st.button(label="criar playlist")
    # st.image("playlist.jpg", caption="Minhas favoritas", width=150)
    # st.subheader("Estatísticas")
    # st.write(
    #     """
    #     Playlists criadas: 1\n
    #     Músicas curtidas: 20\n
    #     Gênero favorito: Pop
    #     """
    # )