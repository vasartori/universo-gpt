# ./frontend/frontend.py
import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Universo GPT", layout="centered")

CHAT_API_URL = os.getenv("CHAT_API_URL", "localhost")
CHAT_API_PORT = os.getenv("CHAT_API_PORT", "5000")

st.markdown("""
    <style>
        .chat-box {
            height: 500px;
            overflow-y: auto;
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            padding: 1rem;
            border-radius: 0.5rem;
            font-family: monospace;
            font-size: 0.9rem;
        }
        .user {
            color: #1f77b4;
            font-weight: bold;
        }
        .bot {
            color: #2ca02c;
            font-weight: bold;
        }
        .message {
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Universo GPT")

# Sessões
if "user_input_temp" not in st.session_state:
    st.session_state.user_input_temp = ""
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "submit" not in st.session_state:
    st.session_state.submit = False

def render_chat(history):
    html = '<div class="chat-box">'
    for msg in history:
        role = "user" if msg["role"] == "user" else "bot"
        content = msg.get("streaming", msg["content"]).replace("\n", "<br>")
        html += f'<div class="message"><span class="{role}">{msg["role"].capitalize()}:</span> {content}</div>'
    html += '</div>'
    return html

# Chat
chat_box = st.empty()
chat_box.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

# Input
def handle_submit():
    st.session_state.submit = True
    st.session_state.user_input_temp = st.session_state.input_text
    st.session_state.input_text = ""

st.text_input(
    "Digite sua mensagem:",
    key="input_text",
    on_change=handle_submit,
    placeholder="Pergunte algo para Sofia...",
    label_visibility="collapsed"
)

if st.session_state.submit and st.session_state.user_input_temp.strip():
    user_input = st.session_state.user_input_temp.strip()
    st.session_state.submit = False

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    chat_box.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

    # Streaming da resposta
    try:
        response = requests.post(
            f"http://{CHAT_API_URL}:{CHAT_API_PORT}/chat",
            json={"message": user_input},
            stream=True,
            timeout=60
        )
        bot_msg = ""
        stream_index = len(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "bot", "content": ""})  # placeholder

        for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
            if chunk:
                bot_msg += chunk
                st.session_state.chat_history[stream_index]["streaming"] = bot_msg
                chat_box.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

        st.session_state.chat_history[stream_index]["content"] = bot_msg

    except Exception as e:
        st.session_state.chat_history.append({"role": "bot", "content": f"Erro: {e}"})

    st.rerun()
