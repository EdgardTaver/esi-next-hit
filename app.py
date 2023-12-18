## pip install streamlit
## pip install streamlit_option_menu
## pip install streamlit_searchbox

## python -m streamlit run app.py

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_searchbox import st_searchbox

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
    st_searchbox(search_function="List", placeholder="Procure por uma música")
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
    st.subheader("Nome do Perfil")
    st.image("axolote.jpg", width=100)
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Minhas playlists")
    with right_column:
        st.button(label="criar playlist")
    st.image("playlist.jpg", caption="Minhas favoritas", width=150)
    st.subheader("Estatísticas")
    st.write(
        """
        Playlists criadas: 1\n
        Músicas curtidas: 20\n
        Gênero favorito: Pop
        """
    )