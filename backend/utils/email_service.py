# backend/utils/email_service.py

import smtplib
from email.message import EmailMessage

# ==============================
# CONFIGURAÇÃO DE EMAIL
# ==============================
SMTP_HOST = "localhost"       # Servidor SMTP local (ex: MailHog ou similar)
SMTP_PORT = 1025              # Porta do servidor SMTP local
FROM_EMAIL = "admin@blogllm.local"

# ==============================
# FUNÇÃO DE ENVIO DE EMAIL DE ATIVAÇÃO
# ==============================
def send_activation_email(email_to: str, token: str) -> bool:
    """
    Envia email de ativação de conta com token.
    Retorna True se enviado com sucesso, False caso contrário.
    """
    msg = EmailMessage()
    msg.set_content(
        f"""
            Olá,

            Sua conta no BlogLLM foi criada com sucesso.

            Para ativar sua conta, utilize o token abaixo:

            {token}

            Depois do login, insira este token na tela de ativação.

            — BlogLLM SOC Platform
            """
    )
    msg["Subject"] = "Ativação de Conta – BlogLLM"
    msg["From"] = FROM_EMAIL
    msg["To"] = email_to

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar email:", e)
        return False