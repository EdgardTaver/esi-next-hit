## python -m streamlit run app.py

import streamlit as st
from streamlit_option_menu import option_menu
from app.frontend.session import initialize_session_variables
from app.frontend.sections import explore_section, playlist_section, profile_section

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
    explore_section()

if selected=="Playlists":
    playlist_section()

if selected=="Perfil":
    profile_section()