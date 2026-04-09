# backend/learning/memory_store.py
import json
from pathlib import Path

# Arquivo de memória local
MEMORY_FILE = Path("backend/learning/memory.json")

# Estrutura padrão
DEFAULT_MEMORY = {
    "logs": [],           # Logs analisados
    "ips": {},            # Contagem de IPs reincidentes
    "semantic_memory": [] # Embeddings de eventos para comparação semântica
}

def load_memory():
    """
    Carrega a memória de logs. Se o arquivo não existir ou estiver corrompido, cria memória padrão.
    """
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except json.JSONDecodeError:
            return DEFAULT_MEMORY.copy()
    else:
        return DEFAULT_MEMORY.copy()

def save_memory(memory):
    """
    Salva a memória atual em disco (JSON).
    """
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))