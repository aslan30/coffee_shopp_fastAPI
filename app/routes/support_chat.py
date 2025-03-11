from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from app.models.support_chat import MessageType
from app.schemas.support_chat import SupportMessageCreate, SupportMessageOut, SupportMessageResponse
from app.services.support_chat import SupportChatService
from app.utils.security import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/support-chat", tags=["support-chat"])


@router.post("/messages", response_model=SupportMessageOut)
async def create_message(
        message_data: SupportMessageCreate,
        current_user: User = Depends(get_current_user),
):
    """Создание нового сообщения в чате поддержки."""
    return await SupportChatService.create_message(current_user.id, message_data)


@router.get("/messages", response_model=list[SupportMessageOut])
async def get_user_messages(current_user: User = Depends(get_current_user)):
    """Получение всех сообщений пользователя."""
    return await SupportChatService.get_user_messages(current_user.id)


@router.post("/messages/{message_id}/respond", response_model=SupportMessageOut)
async def respond_to_message(
        message_id: UUID,
        response_data: SupportMessageResponse,
        current_user: User = Depends(get_current_user),
):
    """Ответ на сообщение в чате поддержки."""
    return await SupportChatService.respond_to_message(message_id, current_user.id, response_data)


@router.get("/admin/messages", response_model=list[SupportMessageOut])
async def get_all_messages(
        limit: int = Query(default=10, description="Количество сообщений на странице", gt=0, le=100),
        offset: int = Query(default=0, description="Смещение для пагинации", ge=0),
        message_type: Optional[MessageType] = Query(None,
                                                    description="Тип сообщения (complaint, question, suggestion)"),
        is_read: Optional[bool] = Query(None, description="Фильтр по прочитанным сообщениям"),
        current_user: User = Depends(get_current_user),
):
    """Получение всех сообщений с пагинацией и фильтрацией (только для поддержки и администратора)."""
    if current_user.role not in [RoleEnum.support, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="You do not have permission to view all messages")
    return await SupportChatService.get_all_messages(limit, offset, message_type, is_read)


@router.post("/admin/cleanup")
async def cleanup_old_chats(current_user: User = Depends(get_current_user)):
    """Удаление старых завершенных чатов (только для администратора)."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    await SupportChatService.delete_old_chats()
    return {"message": "Old chats deleted successfully"}
