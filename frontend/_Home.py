import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

import streamlit as st
from backend.orchestrator import analyze
from backend.db.users_db import login_user, register_user, activate_user
# from backend.utils.email_service import send_activation_email  # desativado por enquanto

st.set_page_config(page_title="BlogLLM SOC", layout="wide")

def hide_sidebar():
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_login_tabs():
    st.title("🔐 BlogLLM SOC")
    tab_login, tab_register, tab_activate = st.tabs(["Login", "Registrar", "Ativar Conta"])

    with tab_login:
        st.subheader("Login")
        login_user_ = st.text_input("Usuário", key="login_user")
        login_pass = st.text_input("Senha", type="password", key="login_pass")
        if st.button("Entrar", key="btn_login"):
            user, err = login_user(login_user_, login_pass)
            if user:
                st.session_state.user = user
                #st.experimental_rerun()
                st.rerun()
            else:
                st.error(err)

    with tab_register:
        st.subheader("Registrar")
        reg_user = st.text_input("Novo Usuário", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Nova Senha", type="password", key="reg_pass")
        if st.button("Registrar", key="btn_register"):
            token = register_user(reg_user, reg_email, reg_pass)
            if token:
                st.success("Usuário criado! Por enquanto, ative a conta na aba 'Ativar Conta'.")
                # send_activation_email(reg_email, token)  # desativado temporariamente
                st.session_state.activation_token = token
            else:
                st.error("Usuário/email já existe.")

    with tab_activate:
        st.subheader("Ativar Conta")
        activation_token = st.text_input("Token de Ativação", key="activate_token")
        if st.button("Ativar", key="btn_activate"):
            if activate_user(activation_token):
                st.success("Conta ativada! Faça login agora.")
            else:
                st.error("Token inválido.")

def show_logged_in_sidebar():
    st.sidebar.title(f"👤 {st.session_state.user['username']}")
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        st.experimental_rerun()

def page_app():
    st.title("🛡️ BlogLLM SOC - Página Principal")
    st.caption("Análise forense inteligente de logs, CSVs e imagens")

    mode = st.radio("Tipo de entrada:", ["Texto / Logs", "Upload de Arquivo"])
    content, ctype = None, None

    if mode == "Texto / Logs":
        content = st.text_area(
            "Cole logs ou texto:",
            height=250,
            placeholder="Ex: Failed login from 192.168.1.1..."
        )
        ctype = "text"

    elif mode == "Upload de Arquivo":
        uploaded_file = st.file_uploader(
            "Escolha CSV, TXT ou imagem",
            type=["txt", "csv", "png", "jpg", "jpeg"]
        )
        if uploaded_file:
            st.info(f"Arquivo carregado: {uploaded_file.name}")
            content_type = uploaded_file.type

            if "text" in content_type or uploaded_file.name.endswith(".txt"):
                content = str(uploaded_file.read(), "utf-8")
                ctype = "text"
                st.code(content[:500], language="text")

            elif "csv" in content_type or uploaded_file.name.endswith(".csv"):
                content = str(uploaded_file.read(), "utf-8")
                ctype = "csv"
                st.code(content[:500], language="csv")

            else:
                content = uploaded_file.read()
                ctype = "image"
                st.image(uploaded_file, caption="Preview da imagem")

    if st.button("🚀 Analisar", use_container_width=True):
        if not content:
            st.warning("Forneça conteúdo para análise.")
        else:
            with st.spinner("A analisar..."):
                result, engine_used, alerts = analyze(content, content_type=ctype)

            st.success("Análise concluída")
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📄 Resultado")
                st.text(result)

            with col2:
                st.subheader("⚙️ Engine")
                st.info(engine_used)

            if alerts:
                st.subheader("🚨 Alertas")
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("Nenhum alerta crítico detectado")

def page_detail():
    st.title("Detalhe")
    st.info("Aqui vai a página de detalhe (em desenvolvimento).")

def page_history():
    st.title("Histórico")
    st.info("Aqui vai a página de histórico (em desenvolvimento).")

def show_app_tabs():
    tabs = st.tabs(["Home", "Detalhe", "Histórico"])
    with tabs[0]:
        page_app()
    with tabs[1]:
    #    page_detail()
    #with tabs[2]:
        page_history()

if "user" not in st.session_state:
    hide_sidebar()
    show_login_tabs()
else:
    show_logged_in_sidebar()
    show_app_tabs()