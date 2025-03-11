from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from config import settings


TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.order",
                "app.models.order_element",
                "app.models.category",
                "app.models.establishment",
                "app.models.support_chat",
                "app.models.menu_item",
                "app.models.basket",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

async def init_db():
    """
    Асинхронная инициализация базы данных.
    Используется для миграций или в асинхронных контекстах.
    """
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

def init_db_sync(app):
    """
    Синхронная регистрация базы данных для FastAPI.
    Используется для интеграции Tortoise ORM с FastAPI.
    """
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )

async def close_db():
    """
    Закрывает соединение с базой данных.
    Используется при завершении работы приложения.
    """
    await Tortoise.close_connections()