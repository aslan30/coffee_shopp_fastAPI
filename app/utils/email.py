import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_verification_email(email: str, verification_code: str):
    """Отправляет email с кодом для подтверждения."""
    subject = "Подтверждение регистрации"
    body = f"Ваш код для подтверждения email: {verification_code}"

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Включаем TLS
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")


send_verification_email("recipient@example.com", "1234")
