# frontend/app.py

import sys
from pathlib import Path

# Adiciona raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

import streamlit as st
from backend.orchestrator import analyze
from backend.db.users_db import login_user, register_user, activate_user
from backend.utils.email_service import send_activation_email

st.set_page_config(page_title="BlogLLM SOC", layout="wide")

# ==============================
# Autenticação
# ==============================
st.sidebar.title("Login")
option = st.sidebar.selectbox("Escolha", ["Login", "Registrar", "Ativar Conta"])

if option == "Registrar":
    st.sidebar.subheader("Novo Usuário")
    username = st.sidebar.text_input("Usuário")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Registrar"):
        token = register_user(username, email, password)
        if token:
            send_activation_email(email, token)
            st.success("Usuário registrado! Verifique seu email para ativação.")
        else:
            st.error("Erro: usuário ou email já existe.")

elif option == "Ativar Conta":
    token = st.sidebar.text_input("Token de Ativação")
    if st.sidebar.button("Ativar"):
        if activate_user(token):
            st.success("Conta ativada com sucesso!")
        else:
            st.error("Token inválido.")

elif option == "Login":
    st.sidebar.subheader("Entrar")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Login"):
        user, err = login_user(username, password)
        if user:
            st.success(f"Bem-vindo {username}!")
            st.session_state.user = user
        else:
            st.error(err)

# ==============================
# Upload e Análise
# ==============================
if "user" in st.session_state:
    st.header("Envie artefactos para análise")
    uploaded_file = st.file_uploader("Escolha um arquivo CSV/Text/Imagem", type=["txt", "csv", "png", "jpg", "jpeg"])

    if uploaded_file:
        content_type = uploaded_file.type
        if "text" in content_type or uploaded_file.name.endswith(".txt"):
            content = str(uploaded_file.read(), "utf-8")
            ctype = "text"
        elif "csv" in content_type or uploaded_file.name.endswith(".csv"):
            content = str(uploaded_file.read(), "utf-8")
            ctype = "csv"
        else:
            content = uploaded_file.read()
            ctype = "image"

        result, engine_used, alerts = analyze(content, content_type=ctype)
        st.subheader(f"Resultado ({engine_used})")
        st.text(result)
        if alerts:
            st.warning("\n".join(alerts))