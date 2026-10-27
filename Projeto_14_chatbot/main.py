
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Configuração da página
st.set_page_config(
    page_title="Chatbot Groq",
    page_icon="🤖",
    layout="centered"
)

# Carrega a chave da API
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Interface
st.title("🤖 Chatbot Groq")
st.caption("Converse com inteligência artificial usando Python")

if not API_KEY:
    st.error(
        "Chave GROQ_API_KEY não encontrada. "
        "Verifique se o arquivo .env está configurado."
    )
    st.stop()

# Cliente Groq
client = Groq(api_key=API_KEY)

# Histórico da conversa
if "historico" not in st.session_state:
    st.session_state.historico = []

# Botão para limpar a conversa
if st.button("🗑️ Limpar conversa"):
    st.session_state.historico = []
    st.rerun()

# Exibe as mensagens anteriores
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Campo de mensagem
pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    # Exibe a mensagem do usuário
    st.session_state.historico.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    # Consulta a IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um assistente prestativo. "
                                "Responda em português de forma clara."
                            )
                        },
                        *st.session_state.historico
                    ]
                )

                texto = resposta.choices[0].message.content
                st.markdown(texto)

                st.session_state.historico.append({
                    "role": "assistant",
                    "content": texto
                })

            except Exception as erro:
                st.error(f"Erro ao consultar a Groq: {erro}")
                # Retira a pergunta que não recebeu resposta
                st.session_state.historico.pop()

