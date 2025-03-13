import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY не загружен! Проверь .env файл.")

    ALGORITHM: str = os.getenv("ALGORITHM")
    if not ALGORITHM:
        raise ValueError("ALGORITHM не загружен! Проверь .env файл.")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    if not ACCESS_TOKEN_EXPIRE_MINUTES:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES не загружен! Проверь .env файл.")

    # Настройки SMTP
    SMTP_USER: str = os.getenv("SMTP_USER")
    if not SMTP_USER:
        raise ValueError("SMTP_USER не загружен! Проверь .env файл.")

    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    if not SMTP_PASSWORD:
        raise ValueError("SMTP_PASSWORD не загружен! Проверь .env файл.")

    SMTP_HOST: str = os.getenv("SMTP_HOST")
    if not SMTP_HOST:
        raise ValueError("SMTP_HOST не загружен! Проверь .env файл.")

    SMTP_PORT: int = int(os.getenv("SMTP_PORT"))
    if not SMTP_PORT:
        raise ValueError("SMTP_PORT не загружен! Проверь .env файл.")

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL не загружен! Проверь .env файл.")

    DEFAULT_ADMIN_PHONE: str = os.getenv("DEFAULT_ADMIN_PHONE")
    if not DEFAULT_ADMIN_PHONE:
        raise ValueError("DEFAULT_ADMIN_PHONE не загружен! Проверь .env файл.")

    DEFAULT_SUPPORT_PHONE: str = os.getenv("DEFAULT_SUPPORT_PHONE")
    if not DEFAULT_SUPPORT_PHONE:
        raise ValueError("DEFAULT_SUPPORT_PHONE не загружен! Проверь .env файл.")


settings = Settings()
