# init_db.py

import sys
from pathlib import Path

# adiciona o diretório raiz ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.db.users_db import init_user_db

init_user_db()
print("Banco de dados de usuários inicializado com sucesso!")