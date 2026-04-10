import streamlit as st
from backend.learning.memory_store import load_memory


def page_historico():
    st.title("📚 Histórico de Análises")
    st.caption("Consulta e exploração de análises anteriores")

    memory = load_memory().get("logs", [])
    if not memory:
        st.info("Ainda não existem análises guardadas.")
        st.stop()

    if "selected_analysis" not in st.session_state:
        st.session_state.selected_analysis = None

    def show_details(entry):
        st.session_state.selected_analysis = entry

    if st.session_state.selected_analysis is None:
        st.subheader("🔎 Filtros")
        col1, col2, col3 = st.columns(3)

        with col1:
            type_filter = st.selectbox(
                "Tipo",
                ["Todos"] + sorted(list(set([m.get("type", "unknown") for m in memory])))
            )

        with col2:
            risk_filter = st.slider("Risco mínimo", 0.0, 1.0, 0.0)

        with col3:
            search = st.text_input("Pesquisar")

        filtered = []
        for m in memory:
            if type_filter != "Todos" and m.get("type") != type_filter:
                continue
            if m.get("risk_score", 0) < risk_filter:
                continue
            if search and search.lower() not in str(m).lower():
                continue
            filtered.append(m)

        filtered = list(reversed(filtered))
        st.divider()

        for i, entry in enumerate(filtered):
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(f"🧾 Análise #{entry.get('id', 'N/A')}")
                    st.caption(entry.get("timestamp", ""))
                    st.write(entry.get("summary", "Sem resumo disponível"))
                    st.write(f"**Engine:** {entry.get('engine', 'N/A')}")

                with col2:
                    st.metric("Risco", entry.get("risk_score", 0))
                    st.write(f"Tipo: {entry.get('type', 'N/A')}")

                st.button(
                    f"Ver detalhes {entry.get('id', 'N/A')}",
                    key=f"btn_details_{entry.get('id', i)}",
                    on_click=show_details,
                    args=(entry,)
                )
                st.divider()

    else:
        entry = st.session_state.selected_analysis
        st.header(f"📄 Detalhes da Análise #{entry.get('id', 'N/A')}")
        st.caption(entry.get("timestamp", ""))

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Tipo:** {entry.get('type', 'N/A')}")
            st.write(f"**Engine:** {entry.get('engine', 'N/A')}")
            st.write(f"**Risco:** {entry.get('risk_score', 0)}")
        with col2:
            st.write("**Alertas:**")
            alerts = entry.get("alerts", [])
            if alerts:
                for a in alerts:
                    st.warning(a)
            else:
                st.success("Nenhum alerta registado")

        st.divider()

        st.subheader("Resumo")
        st.write(entry.get("summary", "Sem resumo"))

        st.subheader("Resultado completo")
        st.text(entry.get("result", "Sem resultado"))

        st.subheader("Conteúdo original")
        content = entry.get("content", "Sem conteúdo disponível")
        if entry.get("type") == "text":
            st.code(content, language="text")
        elif entry.get("type") == "csv":
            st.code(content, language="csv")
        elif entry.get("type") == "image":
            st.write("Conteúdo de imagem armazenado como bytes. Usa a análise forense para ver a evidência.")
        else:
            st.write(content)

        forensic_report = entry.get("forensic_report", {})
        st.subheader("Relatório Forense")
        st.json(forensic_report, expanded=True)

        if forensic_report.get("raw_evidence"):
            st.subheader("Evidência Bruta")
            st.json(forensic_report.get("raw_evidence"), expanded=True)

        if entry.get("similar_logs"):
            st.subheader("Logs Similares")
            st.json(entry.get("similar_logs"), expanded=True)

        if st.button("⬅️ Voltar ao histórico"):
            st.session_state.selected_analysis = None
            st.rerun()