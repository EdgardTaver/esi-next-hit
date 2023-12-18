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

from app.frontend.bff import (do_create_playlist, do_list_playlists, do_login,
                              do_logout, do_register, do_search,
                              do_show_playlist)
from app.frontend.components import list_musics
from app.frontend.session import SESSION_CLEAR_SEARCH_RESULTS, SESSION_PLAYLIST_BEING_EXPLORED, SESSION_SHOULD_DISPLAY_LOGIN, SESSION_SHOULD_DISPLAY_LOGOUT, SESSION_SHOULD_DISPLAY_MUSIC_ADDED, SESSION_SHOULD_EXPLORE_PLAYLIST, SESSION_USER_ID, initialize_session_variables

initialize_session_variables()

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
            list_musics(results, False)

    st.subheader("Descoberta diária")
    st.image(["playlist.jpg", "playlist.jpg", "playlist.jpg"], caption=["Playlist Diária", "Descubra: MPB", "Descubra: Rock"], width=150)
    st.subheader("Músicas recomendadas")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150)
    st.subheader("Pop")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150)
    st.subheader("Eletrônica")
    st.image(["music.png", "music.png", "music.png", "music.png"], caption=["music 1", "music 2", "music 3", "music 4"], width=150) 

if selected=="Playlists":
    if st.session_state[SESSION_USER_ID] is None:
        st.error("Faça login para criar uma playlist")

    elif st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST] is not None:
        if st.button(key="playlist_exploring_go_back", label="Voltar"):
            st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST] = None
            st.session_state[SESSION_PLAYLIST_BEING_EXPLORED] = None
            st.rerun()

        st.header(st.session_state[SESSION_PLAYLIST_BEING_EXPLORED])

        if st.session_state[SESSION_SHOULD_DISPLAY_MUSIC_ADDED]:
            st.success("Música adicionada com sucesso!")
            st.session_state[SESSION_SHOULD_DISPLAY_MUSIC_ADDED] = False

        musics = do_show_playlist(st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST])
        if len(musics) == 0:
            st.warning("Playlist vazia")
        else:
            list_musics(musics, False)

        st.subheader("Adicionar músicas à playlist")
        title = st.text_input("Procure por uma música...", "")
        if title and not st.session_state[SESSION_CLEAR_SEARCH_RESULTS]:
            results = do_search(title)
            if len(results) == 0:
                st.error("Nenhuma música encontrada")
            
            else:
                list_musics(results, True)

        st.session_state[SESSION_CLEAR_SEARCH_RESULTS] = False

    else:
        with st.form(key="create_playlist_form"):
            st.subheader("Crie uma playlist")
            name = st.text_input("Nome da playlist")
            submitted = st.form_submit_button("Criar")
            if submitted:
                response = do_create_playlist(st.session_state[SESSION_USER_ID], name)
                if not response:
                    st.error("Erro ao criar playlist.")
                else:
                    st.success("Playlist criada com sucesso!")
        

        st.subheader("Playlists salvas")
        playlists = do_list_playlists(st.session_state[SESSION_USER_ID])
        if len(playlists) == 0:
            st.warning("Nenhuma playlist encontrada")
        
        else:
            for playlist in playlists:
                col1, col2 = st.columns((1,2.75))
                col1.image("playlist.jpg", width=150)
                col2.subheader(playlist["name"])

                unique_button_key = f"explore_{playlist['id']}"
                if col2.button(key=unique_button_key, label="Explorar"):
                    st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST] = playlist["id"]
                    st.session_state[SESSION_PLAYLIST_BEING_EXPLORED] = playlist["name"]
                    st.rerun()

    # st.subheader("Playlists dos seus gêneros favoritos")
    # st.image(["playlist.jpg", "playlist.jpg", "playlist.jpg", "playlist.jpg"], caption=["Pop", "Eletrônica", "Rock", "Jazz"], width=150)
    

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
            # TODO: just do it directly
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