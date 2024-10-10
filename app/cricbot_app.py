import os
from dotenv import find_dotenv, load_dotenv
import streamlit as st

from services.cricbot_service import CricbotService

load_dotenv(find_dotenv(), override=True)
openai_api_key = os.environ.get('OPENAI_API_KEY')

st.title("💬 Cricbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I am Cricbot. You can ask me questions about cricket"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    cricbot_service = CricbotService(openai_api_key)
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)
    msg = cricbot_service.bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)