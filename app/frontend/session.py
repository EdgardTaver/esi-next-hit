import streamlit as st

SESSION_USER_ID = "user_id"
SESSION_USER_NAME = "user_name"
SESSION_SHOULD_DISPLAY_LOGIN = "should_display_login_success"
SESSION_SHOULD_DISPLAY_LOGOUT = "should_display_logout_message"
SESSION_SHOULD_EXPLORE_PLAYLIST = "should_explore_playlist"
SESSION_PLAYLIST_BEING_EXPLORED = "playlist_being_explored"
SESSION_SHOULD_DISPLAY_MUSIC_ADDED = "should_display_music_added_message"
SESSION_CLEAR_SEARCH_RESULTS = "should_clear_search_results"

def initialize_session_variables():
    if SESSION_USER_ID not in st.session_state:
        st.session_state[SESSION_USER_ID] = None

    if SESSION_USER_NAME not in st.session_state:
        st.session_state[SESSION_USER_NAME] = None

    if SESSION_SHOULD_DISPLAY_LOGIN not in st.session_state:
        st.session_state[SESSION_SHOULD_DISPLAY_LOGIN] = False

    if SESSION_SHOULD_DISPLAY_LOGOUT not in st.session_state:
        st.session_state[SESSION_SHOULD_DISPLAY_LOGOUT] = False

    if SESSION_SHOULD_EXPLORE_PLAYLIST not in st.session_state:
        st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST] = None

    if SESSION_PLAYLIST_BEING_EXPLORED not in st.session_state:
        st.session_state[SESSION_PLAYLIST_BEING_EXPLORED] = None

    if SESSION_SHOULD_DISPLAY_MUSIC_ADDED not in st.session_state:
        st.session_state[SESSION_SHOULD_DISPLAY_MUSIC_ADDED] = False

    if SESSION_CLEAR_SEARCH_RESULTS not in st.session_state:
        st.session_state[SESSION_CLEAR_SEARCH_RESULTS] = False