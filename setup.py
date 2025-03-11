from setuptools import setup, find_packages

setup(
    name="admin_creator",
    version="1.0",
    packages=find_packages(include=["app", "app.*"]),
    entry_points={
        "console_scripts": [
            "create-admin=app.seeder.seeder:run",
        ],
    },
    install_requires=[
        "tortoise-orm[asyncpg]",
        "fastapi",
        "uvicorn",
        "python-dotenv",
    ],
)
