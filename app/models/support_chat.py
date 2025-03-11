from enum import Enum
from tortoise import fields as f
from tortoise.models import Model
from uuid import uuid4


class MessageType(str, Enum):
    COMPLAINT = "complaint"  # Жалоба
    QUESTION = "question"  # Вопрос
    SUGGESTION = "suggestion"  # Предложение


class SupportChat(Model):
    id = f.UUIDField(pk=True, default=uuid4)
    user = f.ForeignKeyField("models.User", related_name="support_messages", on_delete=f.CASCADE)
    message = f.TextField()
    message_type = f.CharEnumField(MessageType, max_length=10)
    response = f.TextField(null=True)
    is_read = f.BooleanField(default=False)
    created_at = f.DatetimeField(auto_now_add=True)
    updated_at = f.DatetimeField(auto_now=True)

    def __str__(self):
        return f"SupportChat(id={self.id}, user={self.user.id})"
