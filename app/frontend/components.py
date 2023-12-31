from typing import Any, Callable, Dict, List

import streamlit as st

from app.frontend.bff import do_add_music_to_playlist, do_get_music_recommendations_for_user, do_search
from app.frontend.session import (SESSION_CLEAR_SEARCH_RESULTS,
                                  SESSION_SHOULD_DISPLAY_MUSIC_ADDED,
                                  SESSION_SHOULD_EXPLORE_PLAYLIST, SESSION_USER_ID)


def no_op_button(unique_key: str, instance: Any, music_id: int):
    pass

def add_to_playlist_button(unique_key: str, instance: Any, music_id: int):
    unique_button_key = f"{unique_key}_add_music"
    if instance.button(key=unique_button_key, label="Adicionar à playlist"):
        response = do_add_music_to_playlist(
            st.session_state[SESSION_SHOULD_EXPLORE_PLAYLIST],
            music_id)

        if not response:
            st.error("Erro ao adicionar música à playlist.")
        else:
            st.session_state[SESSION_SHOULD_DISPLAY_MUSIC_ADDED] = True
            st.session_state[SESSION_CLEAR_SEARCH_RESULTS] = True


def list_musics(unique_key: str, musics: List[Dict[str, Any]], interaction_button: Callable[[str, Any, int], None] = no_op_button):
    i = 1
    
    for music in musics:
        col1, col2 = st.columns((1,2.75))
        col1.image(music["image_url"], width=150)
        col2.subheader(music["title"])
        col2.write(music["artist"])
        col2.write(f"Gênero: {music['genre']}")

        interaction_button(f"{unique_key}_{i}", col2, music["id"])
        i += 1

def music_search_box(unique_key: str, interaction_button: Callable[[str, Any, int], None] = no_op_button):
    music_search_term = st.text_input(key=unique_key, label="Procure por uma música...")
    if music_search_term and not st.session_state[SESSION_CLEAR_SEARCH_RESULTS]:
        results = do_search(music_search_term)
        if len(results) == 0:
            st.error("Nenhuma música encontrada")
        
        else:
            list_musics(f"{unique_key}_regular", results, interaction_button)
    
    else:
        recommendations = do_get_music_recommendations_for_user(st.session_state[SESSION_USER_ID])
        if len(recommendations) > 0:
            st.markdown("**Recomendações:**")
            list_musics(f"{unique_key}_recommendations", recommendations, interaction_button)