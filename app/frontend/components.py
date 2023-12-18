from typing import Any, Dict, List

import streamlit as st

def list_musics(musics: List[Dict[str, Any]]):
    for music in musics:
        col1, col2 = st.columns((1,2.75))
        col1.image(music["image_url"], width=150)
        col2.subheader(music["title"])
        col2.write(music["artist"])
        col2.write(f"Gênero: {music['genre']}")
        col2.button(key=music["id"], label="Adicionar à playlist")
