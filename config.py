import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")

load_dotenv(dotenv_path=env_path)


class Settings:
    """Конфигурация приложения."""

    # Загружаем обязательные переменные окружения с проверкой
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY не загружен! Проверь .env файл.")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Настройки SMTP
    SMTP_USER: str = os.getenv("SMTP_USER")
    if not SMTP_USER:
        raise ValueError("SMTP_USER не загружен! Проверь .env файл.")

    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    if not SMTP_PASSWORD:
        raise ValueError("SMTP_PASSWORD не загружен! Проверь .env файл.")

    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.example.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))

    # Строка подключения к базе данных
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgres://postgres:1234@db:5432/coffee_shop_backend"
    )
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL не загружен! Проверь .env файл.")

    # Настройки телефона
    DEFAULT_ADMIN_PHONE: str = os.getenv("DEFAULT_ADMIN_PHONE", "+998977777777")
    DEFAULT_SUPPORT_PHONE: str = os.getenv("DEFAULT_SUPPORT_PHONE", "+998977777777")

    def __init__(self):
        # Дополнительная проверка, если потребуется
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL не загружен! Проверь .env файл.")


settings = Settings()
