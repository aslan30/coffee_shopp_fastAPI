from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional
from enum import Enum


class DeliveryType(str, Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"


class OrderCreate(BaseModel):
    phoneNumb1: str = Field(..., description="Основной номер телефона", min_length=5, max_length=20)
    phoneNumb2: Optional[str] = Field(None, description="Дополнительный номер телефона", min_length=5, max_length=20)
    pickup_location: str = Field(..., description="Откуда забрать заказ", min_length=5, max_length=120)
    delivery_location: str = Field(..., description="Куда доставить заказ", min_length=5, max_length=120)
    delivery_type: DeliveryType = Field(..., description="Тип доставки (delivery/pickup)")
    establishment_id: Optional[UUID] = Field(None, description="ID заведения для самовывоза")

    @field_validator("phoneNumb1", "phoneNumb2")
    def validate_phone_number(cls, value):
        if value and not value.startswith("+"):
            raise ValueError("Номер телефона должен начинаться с '+'")
        return value


class OrderOut(BaseModel):
    id: UUID
    created_at: datetime
    user_id: UUID
    courier_id: Optional[UUID] = Field(None, description="ID курьера")
    phoneNumb1: str
    phoneNumb2: Optional[str]
    pickup_location: str
    delivery_location: str
    totalPrice: float = Field(..., description="Общая стоимость заказа", ge=0)
    delivery_type: DeliveryType
    status: str = Field(..., description="Статус заказа")
    establishment_id: Optional[UUID]

    class Config:
        from_attributes = True
