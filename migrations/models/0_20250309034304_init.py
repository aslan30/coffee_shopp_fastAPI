from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "profile_picture" VARCHAR(255),
    "role" VARCHAR(20),
    "password" VARCHAR(255) NOT NULL,
    "is_verified" BOOL NOT NULL DEFAULT False,
    "is_active" BOOL NOT NULL DEFAULT True,
    "verification_token" VARCHAR(255),
    "deleted_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "phone" VARCHAR(20),
    "additional_phone" VARCHAR(20),
    "verification_code" VARCHAR(4)
);
COMMENT ON COLUMN "user"."role" IS 'customer: customer\ncourier: courier\nadmin: admin\nsupport: support';
CREATE TABLE IF NOT EXISTS "category" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "image" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "establishment" (
    "id" UUID NOT NULL PRIMARY KEY,
    "location" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "order" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "phoneNumb1" INT NOT NULL,
    "phoneNumb2" INT,
    "location" VARCHAR(120),
    "totalPrice" DECIMAL(10,2) NOT NULL DEFAULT 0,
    "delivery_type" VARCHAR(10) NOT NULL DEFAULT 'delivery',
    "pickup_location" VARCHAR(120) NOT NULL,
    "delivery_location" VARCHAR(120) NOT NULL,
    "status" VARCHAR(10) NOT NULL DEFAULT 'pending',
    "courier_id" UUID REFERENCES "user" ("id") ON DELETE SET NULL,
    "establishment_id" UUID REFERENCES "establishment" ("id") ON DELETE SET NULL,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "order"."delivery_type" IS 'DELIVERY: delivery\nPICKUP: pickup';
COMMENT ON COLUMN "order"."status" IS 'PENDING: pending\nACCEPTED: accepted\nREJECTED: rejected\nCOMPLETED: completed\nCANCELLED: cancelled';
CREATE TABLE IF NOT EXISTS "supportchat" (
    "id" UUID NOT NULL PRIMARY KEY,
    "message" TEXT NOT NULL,
    "message_type" VARCHAR(10) NOT NULL,
    "response" TEXT,
    "is_read" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "supportchat"."message_type" IS 'COMPLAINT: complaint\nQUESTION: question\nSUGGESTION: suggestion';
CREATE TABLE IF NOT EXISTS "menuitem" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "image" VARCHAR(255),
    "description" TEXT,
    "price" DOUBLE PRECISION,
    "category_id" UUID REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orderelement" (
    "id" UUID NOT NULL PRIMARY KEY,
    "quantity" SMALLINT NOT NULL,
    "menu_item_id" UUID NOT NULL REFERENCES "menuitem" ("id") ON DELETE CASCADE,
    "order_id" UUID NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "basket" (
    "id" UUID NOT NULL PRIMARY KEY,
    "quantity" SMALLINT NOT NULL DEFAULT 0,
    "menu_item_id" UUID NOT NULL REFERENCES "menuitem" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
