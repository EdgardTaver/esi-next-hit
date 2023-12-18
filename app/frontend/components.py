from typing import Any, Dict, List

import streamlit as st

from app.frontend.bff import do_add_music_to_playlist
from app.frontend.session import SESSION_SHOULD_EXPLORE_PLAYLIST

def list_musics(musics: List[Dict[str, Any]], show_add_to_playlist: bool):
    print(musics)

    for music in musics:
        col1, col2 = st.columns((1,2.75))
        col1.image(music["image_url"], width=150)
        col2.subheader(music["title"])
        col2.write(music["artist"])
        col2.write(f"Gênero: {music['genre']}")

        if show_add_to_playlist:
            unique_button_key = f"add_music_{music["id"]}"
            if col2.button(key=unique_button_key, label="Adicionar à playlist"):
                response = do_add_music_to_playlist(
                    st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST],
                    music["id"])

                if not response:
                    st.error("Erro ao adicionar música à playlist.")
                else:
                    st.success("Música adicionada com sucesso!")
                
                # st.rerun()

