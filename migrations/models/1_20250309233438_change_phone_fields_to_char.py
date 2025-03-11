from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" ALTER COLUMN "phoneNumb1" TYPE VARCHAR(20) USING "phoneNumb1"::VARCHAR(20);
        ALTER TABLE "order" ALTER COLUMN "phoneNumb2" TYPE VARCHAR(20) USING "phoneNumb2"::VARCHAR(20);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" ALTER COLUMN "phoneNumb1" TYPE INT USING "phoneNumb1"::INT;
        ALTER TABLE "order" ALTER COLUMN "phoneNumb2" TYPE INT USING "phoneNumb2"::INT;"""
