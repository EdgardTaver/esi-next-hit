## pip install streamlit
## pip install streamlit_option_menu
## pip install streamlit_searchbox

## python -m streamlit run app.py

"""
TODOs:

- [ ] Find a new package for this
- [ ] Derive configs from app.config file
"""

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_searchbox import st_searchbox

from app.frontend.bff import do_login, do_logout, do_register, do_search

SESSION_USER_ID = "user_id"
SESSION_SHOULD_DISPLAY_LOGIN = "should_display_login_success"
SESSION_SHOULD_DISPLAY_LOGOUT = "should_display_logout_message"

if SESSION_USER_ID not in st.session_state:
    st.session_state[SESSION_USER_ID] = None

if SESSION_SHOULD_DISPLAY_LOGIN not in st.session_state:
    st.session_state[SESSION_SHOULD_DISPLAY_LOGIN] = False

if SESSION_SHOULD_DISPLAY_LOGOUT not in st.session_state:
    st.session_state[SESSION_SHOULD_DISPLAY_LOGOUT] = False

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
    if st.session_state[SESSION_SHOULD_DISPLAY_LOGIN]:
        st.success("Login realizado com sucesso!")
        st.session_state[SESSION_SHOULD_DISPLAY_LOGIN] = False
    
    if st.session_state[SESSION_SHOULD_DISPLAY_LOGOUT]:
        st.warning("Logout realizado com sucesso. Até breve!")
        st.session_state[SESSION_SHOULD_DISPLAY_LOGOUT] = False
    
    if st.session_state[SESSION_USER_ID] is not None :
        
        st.write("Olá!")
        # TODO: add more info
        logout = st.button(key="logout", label="Logout")
        if logout:
            response = do_logout()
            if not response:
                st.error("Erro ao fazer logout")
            else:
                st.session_state[SESSION_USER_ID] = None
                st.session_state[SESSION_SHOULD_DISPLAY_LOGOUT] = True
    
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
                    st.session_state[SESSION_USER_ID] = login_response
                    st.session_state[SESSION_SHOULD_DISPLAY_LOGIN] = True
        
        with st.form(key="register_form"):
            st.subheader("Não possui uma conta? Cadastre-se!")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Cadastrar")
            if submitted:
                register_response = do_register(email, password)
                if not register_response:
                    st.error("E-mail já cadastrado.")
                else:
                    st.session_state[SESSION_USER_ID] = register_response
                    st.session_state[SESSION_SHOULD_DISPLAY_LOGIN] = True

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