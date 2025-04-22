import os

import streamlit as st
import requests

st.set_page_config(page_title="Universo GPT", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .chat-box {
            height: 400px;
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

# Inicializa histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Limpa input se necessário
if st.session_state.clear_input:
    st.session_state.input = ""
    st.session_state.clear_input = False

# Caixa de chat
chat_html = '<div class="chat-box">'
for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "bot"
    content = msg["content"].replace("\n", "<br>")
    chat_html += f'<div class="message"><span class="{role}">{msg["role"].capitalize()}:</span> {content}</div>'
chat_html += '</div>'

st.markdown(chat_html, unsafe_allow_html=True)

# Input do usuário
user_input = st.text_input("Digite sua mensagem:", key="input")

CHAT_API_URL = os.getenv("CHAT_API_URL", "chat")
CHAT_API_PORT = os.getenv("CHAT_API_PORT", "5000")

if st.button("Enviar"):
    if user_input.strip() != "":
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        try:
            response = requests.post(f"http://{CHAT_API_URL}:{CHAT_API_PORT}/chat", json={"message": user_input})
            data = response.json()
            st.session_state.chat_history.append({"role": "bot", "content": data["reply"]})
        except Exception as e:
            st.session_state.chat_history.append({"role": "bot", "content": f"Erro: {e}"})

        st.session_state.clear_input = True
        st.rerun()
