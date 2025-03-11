import uuid
from tortoise import fields as f
from tortoise.models import Model
from enum import Enum


class RoleEnum(str, Enum):
    customer = 'customer'
    courier = 'courier'
    admin = 'admin'
    support = 'support'


class User(Model):
    id = f.UUIDField(pk=True, default=uuid.uuid4)
    first_name = f.CharField(max_length=50)
    last_name = f.CharField(max_length=50)
    email = f.CharField(max_length=50, unique=True)
    profile_picture = f.CharField(max_length=255, null=True)
    role = f.CharEnumField(RoleEnum, max_length=20, null=True)
    password = f.CharField(max_length=255)
    is_verified = f.BooleanField(default=False)
    is_active = f.BooleanField(default=True)
    verification_token = f.CharField(max_length=255, null=True)
    deleted_at = f.DatetimeField(null=True)
    created_at = f.DatetimeField(auto_now_add=True)
    phone = f.CharField(max_length=20, null=True)
    additional_phone = f.CharField(max_length=20, null=True)
    verification_code = f.CharField(max_length=4, null=True)

    def __str__(self):
        return f"User(id={self.id}, email={self.email})"
