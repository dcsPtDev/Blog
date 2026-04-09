# # frontend/pages/2_📚_Historico.py

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

# import streamlit as st
# from backend.learning.memory_store import load_memory

# st.set_page_config(page_title="Histórico", layout="wide")

# st.title("📚 Histórico de Análises")
# st.caption("Consulta e exploração de análises anteriores")

# # ==========================
# # CARREGAR MEMÓRIA
# # ==========================
# memory = load_memory()
# memory = memory.get("logs", [])

# if not memory:
#     st.info("Ainda não existem análises guardadas.")
#     st.stop()

# # ==========================
# # FILTROS
# # ==========================
# st.subheader("🔎 Filtros")

# col1, col2, col3 = st.columns(3)

# with col1:
#     type_filter = st.selectbox(
#         "Tipo",
#         ["Todos"] + list(set([m.get("type", "unknown") for m in memory]))
#     )

# with col2:
#     risk_filter = st.slider("Risco mínimo", 0.0, 1.0, 0.0)

# with col3:
#     search = st.text_input("Pesquisar")

# # ==========================
# # FILTRAR DADOS
# # ==========================
# filtered = []
# for m in memory:
#     if type_filter != "Todos" and m.get("type") != type_filter:
#         continue
#     if m.get("risk_score", 0) < risk_filter:
#         continue
#     if search and search.lower() not in str(m).lower():
#         continue
#     filtered.append(m)

# # ==========================
# # ORDENAR (mais recentes primeiro)
# # ==========================
# filtered = list(reversed(filtered))
# st.divider()

# # ==========================
# # INICIALIZAR SELECTED_ANALYSIS
# # ==========================
# if "selected_analysis" not in st.session_state:
#     st.session_state.selected_analysis = None

# # ==========================
# # LISTAGEM E DETALHES
# # ==========================
# for i, entry in enumerate(filtered):

#     with st.container():
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.subheader(f"🧾 Análise #{entry.get('id', 'N/A')}")
#             st.caption(entry.get("timestamp", ""))
#             st.write(entry.get("summary", "Sem resumo disponível"))

#         with col2:
#             st.metric("Risco", entry.get("risk_score", 0))
#             st.write(f"Tipo: {entry.get('type', 'N/A')}")

#         # Botão para ver detalhes com key único
#         button_key = f"btn_details_{entry.get('id', i)}"
#         if st.button(f"Ver detalhes {entry.get('id', 'N/A')}", key=button_key):
#             st.session_state.selected_analysis = entry
#             st.experimental_rerun()  # atualiza a página para mostrar aba de detalhe

#         st.divider()

# # ==========================
# # MOSTRAR ABA DE DETALHE SE HOUVER
# # ==========================
# if st.session_state.selected_analysis:
#     entry = st.session_state.selected_analysis
#     st.header(f"📄 Detalhes da Análise #{entry.get('id', 'N/A')}")
#     st.caption(entry.get("timestamp", ""))

#     st.subheader("Resumo")
#     st.write(entry.get("summary", "Sem resumo"))

#     st.subheader("Conteúdo completo / Logs")
#     content = entry.get("content", "Sem conteúdo disponível")
#     if entry.get("type") == "text":
#         st.code(content, language="text")
#     elif entry.get("type") == "csv":
#         st.code(content, language="csv")
#     elif entry.get("type") == "image":
#         st.image(content, caption="Imagem analisada")
#     else:
#         st.write(content)

#     st.subheader("Risco e Metadados")
#     st.write(f"Risco: {entry.get('risk_score', 0)}")
#     st.write(f"Tipo: {entry.get('type', 'N/A')}")

#     if st.button("⬅️ Voltar ao histórico"):
#         st.session_state.selected_analysis = None
#         st.experimental_rerun()

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

# import streamlit as st
# from backend.learning.memory_store import load_memory

# st.set_page_config(page_title="Histórico", layout="wide")

# st.title("📚 Histórico de Análises")
# st.caption("Consulta e exploração de análises anteriores")

# # ==========================
# # CARREGAR MEMÓRIA
# # ==========================
# memory = load_memory()
# memory = memory.get("logs", [])

# if not memory:
#     st.info("Ainda não existem análises guardadas.")
#     st.stop()

# # ==========================
# # FILTROS
# # ==========================
# st.subheader("🔎 Filtros")
# col1, col2, col3 = st.columns(3)
# with col1:
#     type_filter = st.selectbox(
#         "Tipo",
#         ["Todos"] + list(set([m.get("type", "unknown") for m in memory]))
#     )
# with col2:
#     risk_filter = st.slider("Risco mínimo", 0.0, 1.0, 0.0)
# with col3:
#     search = st.text_input("Pesquisar")

# # ==========================
# # FILTRAR DADOS
# # ==========================
# filtered = []
# for m in memory:
#     if type_filter != "Todos" and m.get("type") != type_filter:
#         continue
#     if m.get("risk_score", 0) < risk_filter:
#         continue
#     if search and search.lower() not in str(m).lower():
#         continue
#     filtered.append(m)

# filtered = list(reversed(filtered))
# st.divider()

# # ==========================
# # ABAS DE HISTÓRICO E DETALHE
# # ==========================
# if "selected_analysis" not in st.session_state:
#     st.session_state.selected_analysis = None

# tab_hist, tab_det = st.tabs(["📚 Histórico", "📄 Detalhes"])

# # --- Aba Histórico ---
# with tab_hist:
#     for i, entry in enumerate(filtered):
#         with st.container():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.subheader(f"🧾 Análise #{entry.get('id', 'N/A')}")
#                 st.caption(entry.get("timestamp", ""))
#                 st.write(entry.get("summary", "Sem resumo disponível"))
#             with col2:
#                 st.metric("Risco", entry.get("risk_score", 0))
#                 st.write(f"Tipo: {entry.get('type', 'N/A')}")

#             btn_key = f"btn_details_{entry.get('id', i)}"
#             if st.button(f"Ver detalhes {entry.get('id', 'N/A')}", key=btn_key):
#                 st.session_state.selected_analysis = entry

#             st.divider()

# # --- Aba Detalhes ---
# with tab_det:
#     entry = st.session_state.selected_analysis
#     if entry:
#         st.header(f"📄 Detalhes da Análise #{entry.get('id', 'N/A')}")
#         st.caption(entry.get("timestamp", ""))
#         st.subheader("Resumo")
#         st.write(entry.get("summary", "Sem resumo"))
#         st.subheader("Conteúdo completo / Logs")
#         content = entry.get("content", "Sem conteúdo disponível")
#         if entry.get("type") == "text":
#             st.code(content, language="text")
#         elif entry.get("type") == "csv":
#             st.code(content, language="csv")
#         elif entry.get("type") == "image":
#             st.image(content, caption="Imagem analisada")
#         else:
#             st.write(content)
#         st.subheader("Risco e Metadados")
#         st.write(f"Risco: {entry.get('risk_score', 0)}")
#         st.write(f"Tipo: {entry.get('type', 'N/A')}")
#         if st.button("⬅️ Voltar ao histórico"):
#             st.session_state.selected_analysis = None

# frontend/pages/2_📚_Historico.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

import streamlit as st
from backend.learning.memory_store import load_memory
st.set_page_config(page_title="Histórico", layout="wide")

st.title("📚 Histórico de Análises")
st.caption("Consulta e exploração de análises anteriores")

# ==========================
# CARREGAR MEMÓRIA
# ==========================
memory = load_memory()
memory = memory.get("logs", [])

if not memory:
    st.info("Ainda não existem análises guardadas.")
    st.stop()

# ==========================
# INICIALIZAR SELECTED_ANALYSIS
# ==========================
if "selected_analysis" not in st.session_state:
    st.session_state.selected_analysis = None

# ==========================
# SE NÃO HOUVER SELEÇÃO → MOSTRAR HISTÓRICO
# ==========================

def show_details(entry):
    st.session_state.selected_analysis = entry

if st.session_state.selected_analysis is None:

    # ==========================
    # FILTROS
    # ==========================
    st.subheader("🔎 Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.selectbox(
            "Tipo",
            ["Todos"] + list(set([m.get("type", "unknown") for m in memory]))
        )
    with col2:
        risk_filter = st.slider("Risco mínimo", 0.0, 1.0, 0.0)
    with col3:
        search = st.text_input("Pesquisar")

    # ==========================
    # FILTRAR DADOS
    # ==========================
    filtered = []
    for i, m in enumerate(memory):
        if type_filter != "Todos" and m.get("type") != type_filter:
            continue
        if m.get("risk_score", 0) < risk_filter:
            continue
        if search and search.lower() not in str(m).lower():
            continue
        filtered.append(m)

    filtered = list(reversed(filtered))
    st.divider()

    # ==========================
    # LISTAGEM DE ANÁLISES
    # ==========================
    
    for i, entry in enumerate(filtered):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"🧾 Análise #{entry.get('id', 'N/A')}")
                st.caption(entry.get("timestamp", ""))
                st.write(entry.get("summary", "Sem resumo disponível"))
            with col2:
                st.metric("Risco", entry.get("risk_score", 0))
                st.write(f"Tipo: {entry.get('type', 'N/A')}")

            # btn_key = f"btn_details_{entry.get('id', i)}"
            # if st.button(f"Ver detalhes {entry.get('id', 'N/A')}", key=btn_key):
            #     st.session_state.selected_analysis = entry

            st.button(
                f"Ver detalhes {entry.get('id', 'N/A')}",
                key=f"btn_details_{entry.get('id', i)}",
                on_click=show_details,
                args=(entry,)
            )

            st.divider()

# ==========================
# SE HOUVER SELEÇÃO → MOSTRAR DETALHES
# ==========================
else:
    entry = st.session_state.selected_analysis
    st.header(f"📄 Detalhes da Análise #{entry.get('id', 'N/A')}")
    st.caption(entry.get("timestamp", ""))

    st.subheader("Resumo")
    st.write(entry.get("summary", "Sem resumo"))

    st.subheader("Conteúdo completo / Logs")
    content = entry.get("content", "Sem conteúdo disponível")
    if entry.get("type") == "text":
        st.code(content, language="text")
    elif entry.get("type") == "csv":
        st.code(content, language="csv")
    elif entry.get("type") == "image":
        st.image(content, caption="Imagem analisada")
    else:
        st.write(content)

    st.subheader("Risco e Metadados")
    st.write(f"Risco: {entry.get('risk_score', 0)}")
    st.write(f"Tipo: {entry.get('type', 'N/A')}")

    if st.button("⬅️ Voltar ao histórico"):
        st.session_state.selected_analysis = None