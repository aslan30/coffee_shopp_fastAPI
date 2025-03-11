from pydantic import BaseModel, Field
from uuid import UUID


class BasketCreate(BaseModel):
    menu_item_id: UUID = Field(..., description="ID блюда")
    quantity: int = Field(default=1, description="Количество блюда")


class BasketUpdate(BaseModel):
    quantity: int = Field(..., description="Новое количество блюда")


class BasketOut(BaseModel):
    id: UUID
    quantity: int
    menu_item_id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
