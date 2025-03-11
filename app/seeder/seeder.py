import argparse
import asyncio
from tortoise import Tortoise
from app.models.user import User, RoleEnum
from app.utils.security import hash_password
from config import settings
import getpass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_admin_user(email: str, password: str, first_name: str, last_name: str):
    """Создает администратора."""
    existing_user = await User.filter(email=email).first()
    if existing_user:
        logger.warning(f"Пользователь с email {email} уже существует!")
        return None

    hashed_password = hash_password(password)

    admin = await User.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=RoleEnum.admin,
        password=hashed_password,
        is_verified=True,
        is_active=True,
        phone="+998977777777",
    )
    logger.info(f"Администратор создан: {admin.email}")
    return admin


async def main():
    """Основная функция для создания администратора."""
    try:
        await Tortoise.init(
            db_url=settings.DATABASE_URL,
            modules={"models": ["app.models.user"]},
        )

        parser = argparse.ArgumentParser(description="Создание администратора")
        parser.add_argument("--email", type=str, help="Email администратора")
        parser.add_argument("--password", type=str, help="Пароль администратора")
        parser.add_argument("--first-name", type=str, help="Имя администратора")
        parser.add_argument("--last-name", type=str, help="Фамилия администратора")

        args = parser.parse_args()

        if not args.email:
            args.email = input("Email: ")

        if not args.first_name:
            args.first_name = input("Имя: ")

        if not args.last_name:
            args.last_name = input("Фамилия: ")

        if not args.password:
            args.password = getpass.getpass("Пароль: ")
            password2 = getpass.getpass("Пароль (повторите): ")
            if args.password != password2:
                logger.error("Пароли не совпадают!")
                return

        admin = await create_admin_user(args.email, args.password, args.first_name, args.last_name)

        if admin:
            logger.info(f"Администратор успешно создан: {admin.email}")

    except Exception as e:
        logger.error(f"Ошибка при создании администратора: {e}")
    finally:
        await Tortoise.close_connections()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
