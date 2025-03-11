from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class SupportMessageCreate(BaseModel):
    message: str = Field(..., description="Текст сообщения")
    message_type: str = Field(..., description="Тип сообщения (complaint, question, suggestion)")


class SupportMessageResponse(BaseModel):
    response: str = Field(..., description="Текст ответа")


class SupportMessageOut(BaseModel):
    id: UUID
    user_id: UUID
    message: str
    message_type: str
    response: Optional[str]
    is_read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
