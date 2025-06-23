import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()   

st.set_page_config(
    page_title = "Generative AI Demo", 
    page_icon ='🧠',
    layout = "wide"
    )

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel( model_name="gemini-2.0-flash")

def map_role(role):
    return "assistant" if role == "model" else "user"

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("Generative AI ChatBot")

for message in st.session_state.chat_session.history:
    with st.chat_message(map_role(message.role)):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Type your query here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    response = st.session_state.chat_session.send_message(user_input, stream=True)

    with st.chat_message("assistant"):
        for chunk in response:
            st.markdown(chunk.text)
