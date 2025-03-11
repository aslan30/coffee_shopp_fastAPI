import uuid
from fastapi import Form
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


class LoginForm:
    def __init__(
            self,
            email: str = Form(...),
            password: str = Form(...),
    ):
        self.email = email
        self.password = password


class RoleEnum(str, Enum):
    customer = 'customer'
    courier = 'courier'
    restaurant_owner = 'restaurant_owner'
    admin = 'admin'


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    profile_picture: Optional[str] = None
    password: str
    role: Optional[RoleEnum] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    role: Optional[RoleEnum] = None
    phone: Optional[str] = None
    additional_phone: Optional[str] = None


class UserOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    profile_picture: Optional[str] = None
    role: RoleEnum

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str
