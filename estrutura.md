blogllm/
├─ backend/
│  ├─ analysis/
│  │  ├─ forensic/
│  │  │  ├─ csv_analysis.py
│  │  │  ├─ image_analysis.py
│  │  │  └─ text_analysis.py
│  │  ├─ engine.py
│  │  ├─ local_llm.py
│  │  └─ models.py
│  ├─ learning/
│  │  ├─ correlation_engine.py
│  │  ├─ embedding_engine.py
│  │  ├─ learner.py
│  │  ├─ memory_store.py
│  │  └─ similarity.py
│  ├─ llm/
│  │  ├─ groq_client.py
│  │  ├─ groq_llm.py
│  │  └─ offline_mode.py
│  ├─ db/
│  │  └─ users_db.py
│  ├─ utils/
│  │  └─ email_service.py
│  └─ orchestrator.py
├─ frontend/
│  └─ app.py
├─ data/
│  └─ knowledge.db
├─ .env
└─ requirements.txt