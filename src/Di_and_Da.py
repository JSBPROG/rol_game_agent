import streamlit as st
from ui.streamlit_ui import Ui
from agents.llm import Llm
from data.sys_prompts import story_teller, summarizator

model = Llm(url='http://localhost:11434/v1', api_key="ollama", system_prompt=story_teller)
interface = Ui(model=model)

# Inicializar valores en session_state si no existen
if "story_number" not in st.session_state:
    st.session_state.story_number = None
if "chapter" not in st.session_state:
    st.session_state.chapter = 1
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None

interface.header()
interface.explanations()
interface.show_stories()


selected_story = interface.user_story_selection()

st.session_state.story_number = selected_story

if st.session_state.story_number:
    response = interface.narrate(st.session_state.story_number)
    st.session_state["chapter"] = interface.chapter
    choice = interface.button_choice() 
    
    if choice:
        st.session_state.user_choice = choice
while True:
    response = interface.narrate(st.session_state.story_number,text_response_ai=response,user_response=st.session_state.user_choice)
        
        
