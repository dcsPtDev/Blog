# backend/analysis/local_llm.py
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, AutoTokenizer, AutoModelForCausalLM

# -----------------------------
# CONFIGURAÇÃO DO MODELO LOCAL
# -----------------------------
# MODEL_NAME = "TheBloke/LLaMA-3B-GGML"  # Modelo quantizado GGML
MODEL_NAME = "google/flan-t5-small"  # Alternativa leve para CPU/testes

device = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------
# TOKENIZER
# -----------------------------
try:
    if "llama" in MODEL_NAME.lower():
        tokenizer = LlamaTokenizer.from_pretrained(MODEL_NAME)
    else:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
except Exception as e:
    raise RuntimeError(f"Erro ao carregar tokenizer: {e}")

# -----------------------------
# MODELO
# -----------------------------
try:
    if "llama" in MODEL_NAME.lower():
        model = LlamaForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto" if device == "cuda" else None,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
except Exception as e:
    raise RuntimeError(f"Erro ao carregar modelo: {e}")

# -----------------------------
# FUNÇÃO DE ANÁLISE LOCAL
# -----------------------------
def analyze_local_llm(prompt: str, max_tokens: int = 512) -> str:
    """
    Realiza inferência local com o modelo carregado.
    - prompt: texto de entrada
    - max_tokens: número máximo de tokens gerados
    Retorna texto gerado pelo modelo.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result