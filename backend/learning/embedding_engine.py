# backend/learning/embedding_engine.py
from sentence_transformers import SentenceTransformer
import numpy as np

# Modelo leve para CPU/GPU
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def generate_embedding(text: str) -> np.ndarray:
    """
    Gera vetor de embedding para um texto.
    """
    return model.encode(text, convert_to_numpy=True)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calcula similaridade de cosseno entre dois vetores.
    Retorna valor entre 0 e 1.
    """
    if vec1 is None or vec2 is None or len(vec1) == 0 or len(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
