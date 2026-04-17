# 🧠 Blog AI Cybersecurity Forensics Platform (Local + Cloud LLM)

Sistema de análise forense de logs com inteligência artificial híbrida, combinando **LLMs locais (offline)** e **modelos online**, aplicado a **cybersecurity, threat detection e análise forense automatizada**.

---

## 🚀 Visão Geral

Este projeto implementa uma plataforma de análise de segurança que:

- Analisa logs e ficheiros em tempo real
- Executa análise forense estruturada (text, CSV, image)
- Usa IA local (offline LLaMA ou similar)
- Usa fallback para IA online (ex: Groq / LLM API)
- Aprende com histórico de ataques (memory + embeddings)
- Gera alertas SOC baseados em correlação de eventos

---

## 🧩 Arquitetura

O sistema segue uma arquitetura híbrida modular:


---

## 🛠️ Funcionalidades

### 🔍 Análise Forense
- Detecção de IPs suspeitos
- Análise de autenticação (failed logins)
- Entropia (deteção de ofuscação)
- Base64 / encoding detection
- Análise de imagens (steganography, EXIF, signatures)
- Análise CSV estruturada

---

### 🧠 Inteligência Artificial
- LLM local (offline-first)
- LLM online como fallback
- Avaliação de qualidade de respostas
- Prompt enrichment com contexto forense

---

### 💾 Memory & Learning
- Armazenamento de logs históricos
- Embeddings semânticos (SentenceTransformers)
- Detecção de padrões repetidos
- Learning engine baseado em similaridade

---

### ⚠️ SOC / Correlation Engine
- Reincidência de IPs
- Padrões repetitivos de ataques
- Alertas automáticos de segurança
- Correlação de eventos recentes

---

### 👤 Sistema de Utilizadores
- Autenticação com bcrypt
- Gestão de tokens por utilizador
- Controlo de acesso (roles)
- Estatísticas de uso

---

## 🧠 Tecnologias Utilizadas

- Python 3.10+
- Streamlit (frontend)
- SentenceTransformers (embeddings)
- SQLite (users database)
- bcrypt (security)
- NumPy
- PIL (image forensics)
- LLM local (LLaMA-based)
- LLM online (Groq / API fallback)

---

## 📁 Estrutura do Projeto


backend/
│
├── analysis/ # Forensic engines (text, csv, image)
├── detectors/ # Low-level detection (IP, auth, encoding)
├── forensic/ # Specialized analysis modules
├── llm/ # Offline + online LLM integration
├── learning/ # Memory, embeddings, correlation, learning
├── db/ # SQLite user management
├── utils/ # Helpers
│
frontend/
│ └── Streamlit UI
│
data/


---

## 🔄 Fluxo de Execução

1. Utilizador envia log ou ficheiro
2. Sistema executa análise forense estruturada
3. Gera `AnalysisReport` com findings
4. Correlation engine identifica padrões
5. Embeddings são gerados e comparados com memória
6. LLM local processa o contexto
7. Se qualidade for baixa → fallback para LLM online
8. Resposta final é retornada ao utilizador

---

## 🧪 Exemplo de Output

```json
{
  "artifact_type": "text_log",
  "findings": [
    {
      "category": "authentication",
      "severity": "high",
      "description": "Falha de autenticação detetada",
      "confidence": 0.85
    }
  ],
  "risk_level": "high"
}


