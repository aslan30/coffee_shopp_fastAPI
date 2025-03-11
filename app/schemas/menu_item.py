import uuid
from pydantic import BaseModel, Field
from typing import Optional


class MenuItemCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Название элемента меню")
    image: Optional[str] = Field(None, max_length=255, description="Ссылка на изображение")
    description: Optional[str] = Field(None, description="Описание элемента меню")
    price: Optional[float] = Field(None, description="Цена элемента меню")
    category_id: Optional[uuid.UUID] = Field(None, description="ID категории")


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Название элемента меню")
    image: Optional[str] = Field(None, max_length=255, description="Ссылка на изображение")
    description: Optional[str] = Field(None, description="Описание элемента меню")
    price: Optional[float] = Field(None, description="Цена элемента меню")
    category_id: Optional[uuid.UUID] = Field(None, description="ID категории")


class MenuItemOut(BaseModel):
    id: uuid.UUID
    name: str
    image: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category_id: Optional[uuid.UUID]

    class Config:
        from_attributes = True
