# backend/utils/email_service.py
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


# ==============================
# CONFIGURAÇÃO DE EMAIL
# ==============================
SMTP_HOST = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
USER = os.getenv("EMAIL_USER")
PASS = os.getenv("EMAIL_PASS") 


def send_activation_email(email_to: str, token: str) -> bool:
    msg = EmailMessage()

    msg.set_content(f"""
Olá,

Sua conta no BlogLLM foi criada com sucesso.

Para ativar sua conta, utilize o token abaixo:

{token}

— BlogLLM SOC Platform
""")

    msg["Subject"] = "Ativação de Conta – BlogLLM"
    msg["From"] = "no-reply@blogllm.local"
    msg["To"] = email_to

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()              # 🔥 obrigatório
            smtp.login(USER, PASS)       # 🔥 obrigatório
            smtp.send_message(msg)

        print("Email enviado com sucesso")
        return True

    except Exception as e:
        print("Erro ao enviar email:", e)
        return False