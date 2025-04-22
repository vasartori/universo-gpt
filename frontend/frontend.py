# ./frontend/frontend.py
import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Sofia IA", layout="centered")

CHAT_API_URL = os.getenv("CHAT_API_URL", "localhost")
CHAT_API_PORT = os.getenv("CHAT_API_PORT", "5000")

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-p..." crossorigin="anonymous" referrerpolicy="no-referrer" />
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 2rem;
        }
        .chat-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            border: 1px solid #e6e6e6;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .message.user {
            background-color: #eef2ff;
            color: #1e40af;
            align-self: flex-end;
        }
        .message.bot {
            background-color: #ecfdf5;
            color: #064e3b;
            align-self: flex-start;
        }
        .message {
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            max-width: 85%;
            white-space: pre-wrap;
        }
        .message i {
            margin-right: 0.5rem;
            font-size: 1rem;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            height: 60vh;
            overflow-y: auto;
            padding: 0.5rem;
        }
        .footer {
            text-align: center;
            font-size: 0.8rem;
            color: #888888;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <h1>🤖 Sofia IA</h1>
    <p>Assistente virtual com inteligência artificial — pronta para ajudar.</p>
</div>
""", unsafe_allow_html=True)

# Estados da sessão
if "user_input_temp" not in st.session_state:
    st.session_state.user_input_temp = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "submit" not in st.session_state:
    st.session_state.submit = False

def render_chat(messages):
    html = '<div class="chat-container">'
    for msg in messages:
        role = msg["role"]
        content = msg.get("streaming", msg["content"])
        icon = '<i class="fas fa-user"></i>' if role == "user" else '<i class="fas fa-robot"></i>'
        html += f'<div class="message {role}">{icon} {content}</div>'
    html += '</div>'
    return html

chat_area = st.empty()
chat_area.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

# Input
def handle_submit():
    st.session_state.submit = True
    st.session_state.user_input_temp = st.session_state.input_text
    st.session_state.input_text = ""

st.text_input(
    "Digite sua dúvida...",
    key="input_text",
    on_change=handle_submit,
    placeholder="Pergunte algo para a Sofia...",
    label_visibility="collapsed"
)

# Envio
if st.session_state.submit and st.session_state.user_input_temp.strip():
    user_input = st.session_state.user_input_temp.strip()
    st.session_state.submit = False

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    chat_area.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

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
                chat_area.markdown(render_chat(st.session_state.chat_history), unsafe_allow_html=True)

        st.session_state.chat_history[stream_index]["content"] = bot_msg

    except Exception as e:
        st.session_state.chat_history.append({"role": "bot", "content": f"Erro: {e}"})

    st.rerun()

# Rodapé
st.markdown("""
<div class="footer">
    Sofia IA é um projeto experimental. Dúvidas ou sugestões? Fale com a equipe responsável.
</div>
""", unsafe_allow_html=True)
