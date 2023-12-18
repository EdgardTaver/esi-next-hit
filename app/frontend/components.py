from typing import Any, Callable, Dict, List

import streamlit as st

from app.frontend.bff import do_add_music_to_playlist
from app.frontend.session import (SESSION_CLEAR_SEARCH_RESULTS,
                                  SESSION_SHOULD_DISPLAY_MUSIC_ADDED,
                                  SESSION_SHOULD_EXPLORE_PLAYLIST)


def no_op_button(instance: Any, music_id: int):
    pass

def add_to_playlist_button(instance: Any, music_id: int):
    unique_button_key = f"add_music_{music_id}"
    if instance.button(key=unique_button_key, label="Adicionar à playlist"):
        response = do_add_music_to_playlist(
            st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST],
            music_id)

        if not response:
            st.error("Erro ao adicionar música à playlist.")
        else:
            st.session_state[SESSION_SHOULD_DISPLAY_MUSIC_ADDED] = True
            st.session_state[SESSION_CLEAR_SEARCH_RESULTS] = True
            st.rerun()

def list_musics(musics: List[Dict[str, Any]], interaction_button: Callable[[Any, int], None] = no_op_button):
    for music in musics:
        col1, col2 = st.columns((1,2.75))
        col1.image(music["image_url"], width=150)
        col2.subheader(music["title"])
        col2.write(music["artist"])
        col2.write(f"Gênero: {music['genre']}")

        interaction_button(col2, music["id"])

