import os
import streamlit as st
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
st.title("🤖 Meu Assistente IA")

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    if mensagem["role"] == "user":
        with st.chat_message("user"):
            st.write(mensagem["content"])
    else:
        with st.chat_message("assistant"):
            st.write(mensagem["content"])

pergunta = st.chat_input("Digite sua mensagem aqui...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})
    
    with st.chat_message("user"):
        st.write(pergunta)

    resposta = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system="Você é um assistente prestativo. Responda sempre em português.",
        messages=st.session_state.historico
    )

    texto = resposta.content[0].text
    st.session_state.historico.append({"role": "assistant", "content": texto})

    with st.chat_message("assistant"):
        st.write(texto)