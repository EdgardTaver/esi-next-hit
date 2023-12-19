import streamlit as st

from app.frontend.bff import (do_create_playlist, do_list_playlists, do_login,
                              do_logout, do_register, do_get_random_music_recommendations,
                              do_show_playlist)
from app.frontend.components import add_to_playlist_button, list_musics, music_search_box
from app.frontend.session import (SESSION_CLEAR_SEARCH_RESULTS,
                                  SESSION_PLAYLIST_BEING_EXPLORED,
                                  SESSION_SHOULD_DISPLAY_LOGIN,
                                  SESSION_SHOULD_DISPLAY_LOGOUT,
                                  SESSION_SHOULD_DISPLAY_MUSIC_ADDED,
                                  SESSION_SHOULD_EXPLORE_PLAYLIST,
                                  SESSION_USER_ID)

def explore_section():
    music_search_box("explore_search_bar")

    random_recommendations = do_get_random_music_recommendations()
    if len(random_recommendations) > 0:
        st.subheader("Descubra novidades")
        list_musics(random_recommendations)

def playlist_section():
    if st.session_state[SESSION_USER_ID] is None:
        st.error("Faça login para criar uma playlist")

    elif st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST] is not None:
        explore_playlist_section()

    else:
        list_playlists_section()

def explore_playlist_section():
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
        list_musics(musics)

    st.subheader("Adicionar músicas à playlist")
    
    music_search_box("playlist_search_bar", add_to_playlist_button)

    st.session_state[SESSION_CLEAR_SEARCH_RESULTS] = False

def list_playlists_section():
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

def profile_section():
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