import uuid
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.menu_item import MenuItemOut


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Название категории")
    image: Optional[str] = Field(None, max_length=255, description="Ссылка на изображение")


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Название категории")
    image: Optional[str] = Field(None, max_length=255, description="Ссылка на изображение")


class CategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    image: Optional[str]
    items: List[MenuItemOut] = []

    class Config:
        from_attributes = True
