# backend/db/users_db.py
import sqlite3
from pathlib import Path
import json
from datetime import datetime
import bcrypt
import secrets

# ==============================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==============================
DB_PATH = Path("data/knowledge.db")

# ==============================
# INICIALIZAÇÃO DO BANCO DE DADOS
# ==============================
def init_user_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        is_active INTEGER DEFAULT 0,
        activation_token TEXT UNIQUE,
        created_at TEXT,
        last_login TEXT,
        token_limit INTEGER DEFAULT 100,
        tokens_remaining INTEGER DEFAULT 100,
        stats TEXT
    )
    """)

    conn.commit()
    conn.close()

# ==============================
# SEGURANÇA DE SENHA
# ==============================
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ==============================
# REGISTRO DE USUÁRIO
# ==============================
def register_user(username, email, password, role="user", token_limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    password_hash = hash_password(password)
    activation_token = secrets.token_urlsafe(24)
    now = datetime.utcnow().isoformat()

    stats = {
        "queries": 0,
        "alerts_detected": 0,
        "files_uploaded": 0
    }

    try:
        c.execute("""
            INSERT INTO users (
                username, email, password_hash, role,
                is_active, activation_token,
                created_at, token_limit, tokens_remaining, stats
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            email,
            password_hash,
            role,
            0,
            activation_token,
            now,
            token_limit,
            token_limit,
            json.dumps(stats)
        ))

        conn.commit()
        return activation_token

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()

# ==============================
# ATIVAÇÃO DE CONTA
# ==============================
def activate_user(token: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET is_active = 1,
            activation_token = NULL
        WHERE activation_token = ?
    """, (token,))

    updated = c.rowcount
    conn.commit()
    conn.close()
    return updated > 0

# ==============================
# LOGIN
# ==============================
def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT id, password_hash, role, is_active,
               tokens_remaining, token_limit, stats
        FROM users
        WHERE username = ?
    """, (username,))

    row = c.fetchone()

    if not row:
        conn.close()
        return None, "Usuário ou senha incorretos"

    user_id, pw_hash, role, is_active, tokens, limit_, stats = row

    if not is_active:
        conn.close()
        return None, "Conta não ativada"

    if not check_password(password, pw_hash):
        conn.close()
        return None, "Usuário ou senha incorretos"

    # Atualiza último login
    c.execute(
        "UPDATE users SET last_login=? WHERE id=?",
        (datetime.utcnow().isoformat(), user_id)
    )
    conn.commit()
    conn.close()

    return {
        "id": user_id,
        "username": username,
        "role": role,
        "tokens_remaining": tokens,
        "token_limit": limit_,
        "stats": json.loads(stats) if stats else {}
    }, None

# ==============================
# GERENCIAMENTO DE TOKENS
# ==============================
def decrement_tokens(username, amount=1) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET tokens_remaining = tokens_remaining - ?
        WHERE username = ?
          AND tokens_remaining >= ?
    """, (amount, username, amount))

    updated = c.rowcount
    conn.commit()
    conn.close()
    return updated > 0

def reset_tokens(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET tokens_remaining = token_limit
        WHERE username = ?
    """, (username,))

    conn.commit()
    conn.close()

# ==============================
# MÉTRICAS / ESTATÍSTICAS
# ==============================
def increment_stat(username, field):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT stats FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if not row:
        conn.close()
        return

    stats = json.loads(row[0]) if row[0] else {}
    stats[field] = stats.get(field, 0) + 1

    c.execute(
        "UPDATE users SET stats=? WHERE username=?",
        (json.dumps(stats), username)
    )
    conn.commit()
    conn.close()

# ==============================
# FUNÇÕES ADMINISTRATIVAS
# ==============================
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT id, username, email, role,
               is_active, tokens_remaining,
               token_limit, stats, last_login
        FROM users
    """)

    users = []
    for row in c.fetchall():
        (
            id_, username, email, role,
            active, tokens, limit_, stats, last_login
        ) = row

        users.append({
            "id": id_,
            "username": username,
            "email": email,
            "role": role,
            "is_active": bool(active),
            "tokens_remaining": tokens,
            "token_limit": limit_,
            "stats": json.loads(stats) if stats else {},
            "last_login": last_login
        })

    conn.close()
    return users

def set_user_active(username, active: bool):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET is_active=? WHERE username=?",
        (1 if active else 0, username)
    )
    conn.commit()
    conn.close()

def set_user_role(username, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET role=? WHERE username=?",
        (role, username)
    )
    conn.commit()
    conn.close()