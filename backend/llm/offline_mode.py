# # backend/llm/offline_mode.py
import re


def analyze_offline(content, content_type, analysis_type=None, memory=None):
    signals, risks, recommendations = [], [], []

    if isinstance(content, dict):
        artifact_type = content.get("artifact_type", "unknown")
        findings = content.get("findings", [])
        raw = content.get("raw_evidence", {})

        if findings:
            signals.append(f"Relatório forense recebido para {artifact_type}.")

        for finding in findings:
            category = finding.get("category", "unknown")
            severity = finding.get("severity", "medium")
            description = finding.get("description", "")
            evidence = finding.get("evidence", "")
            confidence = finding.get("confidence", 0)

            signals.append(f"{category}: {description}")

            if severity == "high":
                risks.append(f"Achado crítico em {category}: {description}")
            elif severity == "medium":
                risks.append(f"Achado relevante em {category}: {description}")

            if category == "authentication":
                recommendations.append("Investigar tentativas de login falhadas e aplicar proteção contra brute force.")

            elif category == "network":
                recommendations.append("Verificar reputação dos IPs e correlacionar com eventos recentes.")

            elif category == "encoding":
                recommendations.append("Validar se o conteúdo codificado é legítimo antes de qualquer abertura ou execução.")

            elif category == "hidden_data":
                recommendations.append("Analisar strings ocultas com cautela, pois podem conter payloads ou indicadores suspeitos.")

            elif category == "embedded_file":
                recommendations.append("Extrair e analisar o ficheiro embutido em ambiente isolado.")

            elif category == "metadata":
                recommendations.append("Rever EXIF e metadados por possível fuga de informação.")

            elif category == "steganography":
                recommendations.append("Executar análise aprofundada da imagem para confirmar possível esteganografia.")

        if raw.get("ips"):
            signals.append(f"IPs extraídos: {', '.join(raw.get('ips', []))}")

        if raw.get("hidden_strings"):
            preview = raw.get("hidden_strings", [])[:5]
            signals.append(f"Strings ocultas encontradas: {', '.join(preview)}")

        if raw.get("embedded_files"):
            signals.append(f"Ficheiros embutidos possivelmente detetados: {', '.join(raw.get('embedded_files', []))}")

        if raw.get("exif"):
            signals.append(f"EXIF presente com {len(raw.get('exif', {}))} campos.")

        if "entropy" in raw:
            if raw["entropy"] > 7.5:
                risks.append("Entropia muito alta pode indicar ofuscação, compressão anómala ou esteganografia.")
            elif raw["entropy"] > 4.5:
                risks.append("Entropia elevada pode indicar conteúdo ofuscado.")

    else:
        if content_type == "text":
            text_lower = str(content).lower()

            if any(k in text_lower for k in ["erro", "denied", "falha", "failed"]):
                signals.append("Eventos de erro ou falha de acesso detectados.")
                risks.append("Possível problema de autenticação ou permissões.")

            if "login" in text_lower and ("falha" in text_lower or "failed" in text_lower):
                signals.append("Tentativa de login falhada identificada.")
                risks.append("Possível tentativa de brute force ou credenciais inválidas.")
                recommendations.append("Monitorizar múltiplas falhas de login e aplicar rate limiting.")

            import re
            ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ips = list(set(re.findall(ip_pattern, text_lower)))
            if ips:
                signals.append(f"Endereços IP detectados: {', '.join(ips)}")
                risks.append("IPs podem indicar origem de acesso ou atividade suspeita.")
                recommendations.append("Verificar reputação dos IPs e padrões de acesso.")

        elif content_type == "csv":
            lines = str(content).strip().splitlines()
            if len(lines) > 1:
                signals.append(f"CSV contém {len(lines) - 1} linhas de dados.")
            else:
                signals.append("CSV contém apenas cabeçalho ou está vazio.")

        elif content_type == "image":
            signals.append("Imagem recebida para análise.")
            recommendations.append("Utilizar o relatório forense para extrair strings, EXIF e possíveis ficheiros embutidos.")

    if not signals:
        signals.append("Nenhum sinal relevante identificado.")

    success = any([
        len(risks) > 0,
        len(recommendations) > 0,
        any(s != "Nenhum sinal relevante identificado." for s in signals)
    ])

    return {
        "signals": signals,
        "risks": risks,
        "recommendations": recommendations,
        "summary": " | ".join(signals[:2]) if signals else "Sem sinais relevantes"
    }, success