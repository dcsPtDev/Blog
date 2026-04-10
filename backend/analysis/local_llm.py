# # backend/analysis/local_llm.py

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-small"


@st.cache_resource
def load_model():
    """Carrega o modelo uma única vez."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    
    return tokenizer, model


def build_prompt(report_dict: dict) -> str:
    # [mantém o mesmo código que já tens]
    artifact_type = report_dict.get("artifact_type", "unknown")
    risk_level = report_dict.get("risk_level", "low")
    findings = report_dict.get("findings", [])
    raw_evidence = report_dict.get("raw_evidence", {})

    findings_text = []
    for f in findings:
        findings_text.append(
            f"{f.get('category', 'unknown')} | {f.get('severity', 'medium')} | {f.get('description', '')} | {f.get('evidence', '')}"
        )

    prompt = f"""
            You are a cybersecurity analyst.
            Analyze the forensic report and return:
            1. A short summary
            2. Main risks
            3. Practical recommendations #MOST IMPORTANT#
            4. User-friendly explanation

            Artifact type: {artifact_type}
            Risk level: {risk_level}

            Findings:
            {chr(10).join('- ' + x for x in findings_text)}

            Raw evidence:
            {raw_evidence}

            Write concise, clear and practical output.
            

            """
    return prompt.strip()


def analyze_local_llm(report_dict: dict, max_tokens: int = 256) -> str:
    tokenizer, model = load_model()  # ← Carrega só uma vez!
    
    prompt = build_prompt(report_dict)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=False
    )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result