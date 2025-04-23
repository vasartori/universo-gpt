# frontend/frontend.py
import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Assistente IA", layout="centered")

CHAT_API_URL = os.getenv("CHAT_API_URL", "localhost")
CHAT_API_PORT = os.getenv("CHAT_API_PORT", "5000")

# Título
st.markdown("""
<div style='text-align: center; font-size: 36px; font-weight: bold;'>
    🤖 Assistente IA
</div>
<p style='text-align: center; font-size: 16px;'>Converse com uma IA conectada ao seu próprio backend</p>
<hr>
""", unsafe_allow_html=True)

# Inicializa estado da sessão
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Renderiza histórico
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            response = requests.post(
                f"http://{CHAT_API_URL}:{CHAT_API_PORT}/chat",
                json={"message": user_input},
                stream=True,
                timeout=60
            )
            assistant_reply = ""
            for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                if chunk:
                    assistant_reply += chunk
                    placeholder.markdown(assistant_reply)
        except Exception as e:
            assistant_reply = f"Erro ao gerar resposta: {e}"
            placeholder.error(assistant_reply)

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

# Rodapé
st.markdown("""
<div style="text-align: center; font-size: 0.8rem; color: #888; margin-top: 2rem;">
    Assistente IA é um projeto experimental. Dúvidas ou sugestões? Fale com a equipe responsável.
</div>
""", unsafe_allow_html=True)
