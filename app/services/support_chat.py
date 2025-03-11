from fastapi import WebSocket, HTTPException
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from app.models.support_chat import SupportChat, MessageType
from app.models.user import User, RoleEnum
from app.schemas.support_chat import SupportMessageCreate, SupportMessageOut, SupportMessageResponse


class SupportService:
    """Сервис для обработки WebSocket-сообщений поддержки."""

    active_support_connections: List[WebSocket] = []
    active_client_connections: Dict[str, WebSocket] = {}

    @classmethod
    async def connect_client(cls, websocket: WebSocket):
        """Подключение клиента."""
        await websocket.accept()
        client_id = str(id(websocket))
        cls.active_client_connections[client_id] = websocket
        await websocket.send_text("You are connected as client.")

        for support_ws in cls.active_support_connections:
            await support_ws.send_text(f"New client connected: {client_id}")

    @classmethod
    async def disconnect_client(cls, websocket: WebSocket):
        """Отключение клиента."""
        client_id = str(id(websocket))
        cls.active_client_connections.pop(client_id, None)
        await websocket.close()

        for support_ws in cls.active_support_connections:
            await support_ws.send_text(f"Client disconnected: {client_id}")

    @classmethod
    async def handle_client_message(cls, websocket: WebSocket, data: str):
        """Обработка сообщений от клиента."""
        client_id = str(id(websocket))
        for support_ws in cls.active_support_connections:
            await support_ws.send_text(f"Client {client_id}: {data}")

    @classmethod
    async def connect_support(cls, websocket: WebSocket):
        """Подключение поддержки."""
        await websocket.accept()
        cls.active_support_connections.append(websocket)
        await websocket.send_text("You are connected as support.")

    @classmethod
    async def disconnect_support(cls, websocket: WebSocket):
        """Отключение поддержки."""
        cls.active_support_connections.remove(websocket)
        await websocket.close()

    @classmethod
    async def handle_support_message(cls, websocket: WebSocket, data: str):
        """Обработка сообщений от поддержки."""
        if data.startswith("to_client:"):
            _, client_id, message = data.split(":", 2)
            if client_id in cls.active_client_connections:
                await cls.active_client_connections[client_id].send_text(f"Support: {message}")
            else:
                await websocket.send_text(f"Client {client_id} is not connected.")
        else:
            await websocket.send_text(f"Unknown command: {data}")


class SupportChatService:
    @staticmethod
    async def create_message(user_id: UUID, message_data: SupportMessageCreate) -> SupportMessageOut:
        """Создание нового сообщения в чате поддержки."""
        message = await SupportChat.create(user_id=user_id, **message_data.dict())
        return SupportMessageOut(**message.__dict__)

    @staticmethod
    async def get_user_messages(user_id: UUID) -> list[SupportMessageOut]:
        """Получение всех сообщений пользователя."""
        messages = await SupportChat.filter(user_id=user_id).all()
        return [SupportMessageOut(**message.__dict__) for message in messages]

    @staticmethod
    async def respond_to_message(message_id: UUID, responder_id: UUID,
                                 response_data: SupportMessageResponse) -> SupportMessageOut:
        """Ответ на сообщение в чате поддержки."""
        try:
            message = await SupportChat.get(id=message_id)
            responder = await User.get(id=responder_id)

            # Проверяем, что отвечающий имеет права (support или admin)
            if responder.role not in [RoleEnum.support, RoleEnum.admin]:
                raise HTTPException(status_code=403, detail="You do not have permission to respond to messages")

            message.response = response_data.response
            message.is_read = True
            await message.save()
            return SupportMessageOut(**message.__dict__)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Message not found")

    @staticmethod
    async def get_all_messages(
            limit: int = 10,
            offset: int = 0,
            message_type: Optional[MessageType] = None,
            is_read: Optional[bool] = None,
    ) -> list[SupportMessageOut]:
        """Получение всех сообщений с пагинацией и фильтрацией."""
        query = SupportChat.all()
        if message_type:
            query = query.filter(message_type=message_type)
        if is_read is not None:
            query = query.filter(is_read=is_read)
        messages = await query.offset(offset).limit(limit).all()
        return [SupportMessageOut(**message.__dict__) for message in messages]

    @staticmethod
    async def delete_old_chats():
        """Удаление завершенных чатов старше 3 месяцев."""
        three_months_ago = datetime.now() - timedelta(days=90)
        await SupportChat.filter(response__isnull=False, created_at__lt=three_months_ago).delete()
