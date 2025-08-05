import streamlit as st
from ui.streamlit_ui import Ui
from agents.llm import Llm
from data.sys_prompts import story_teller

# --- Inicialización ---
model = Llm(url='http://localhost:11434/v1', api_key="ollama", system_prompt=story_teller)
interface = Ui(model=model)

# --- Estado de la sesión ---
if "story_number" not in st.session_state:
    st.session_state.story_number = None
if "chapter" not in st.session_state:
    st.session_state.chapter = 1
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None
if "story_text" not in st.session_state:
    st.session_state.story_text = ""

# --- Interfaz de usuario ---
interface.header()
interface.explanations()
interface.show_stories()

# --- Selección de historia ---
selected_story = interface.user_story_selection()
if selected_story != st.session_state.story_number:
    # Si el usuario elige una nueva historia, reinicia el estado
    st.session_state.story_number = selected_story
    st.session_state.chapter = 1
    st.session_state.user_choice = None
    st.session_state.story_text = ""

# --- Lógica del juego ---
if st.session_state.story_number:
    interface.chapter = st.session_state.chapter

    if st.session_state.chapter == 1 and not st.session_state.story_text:
        # Inicia el primer capítulo
        st.session_state.story_text = interface.narrate(st.session_state.story_number)
        st.session_state.chapter += 1

    # Muestra el texto de la historia
    if st.session_state.story_text:
        st.write(st.session_state.story_text)

    # Muestra los botones de elección
    choice = interface.button_choice()
    if choice:
        st.session_state.user_choice = choice
        # Genera el siguiente capítulo basado en la elección del usuario
        st.session_state.story_text = interface.narrate(
            st.session_state.story_number,
            text_response_ai=st.session_state.story_text,
            user_response=st.session_state.user_choice
        )
        st.session_state.chapter += 1
        # Vuelve a ejecutar para mostrar el nuevo texto
        st.rerun()
        
        
