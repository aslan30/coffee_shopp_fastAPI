from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from app.models.basket import Basket
from app.models.menu_item import MenuItem
from app.models.user import User
from uuid import UUID

from app.schemas.basket import BasketOut


class BasketService:
    @staticmethod
    async def add_to_basket(user_id: UUID, menu_item_id: UUID, quantity: int = 1):
        """Добавление блюда в корзину."""
        menu_item = await MenuItem.get(id=menu_item_id)
        user = await User.get(id=user_id)

        basket, created = await Basket.get_or_create(
            menu_item=menu_item,
            user=user,
            defaults={"quantity": quantity}
        )
        if not created:
            basket.quantity += quantity
            await basket.save()

        return basket

    @staticmethod
    async def remove_from_basket(user_id: UUID, menu_item_id: UUID):
        """Удаление блюда из корзины."""
        await Basket.filter(user_id=user_id, menu_item_id=menu_item_id).delete()

    @staticmethod
    async def get_user_basket(user_id: UUID):
        """Получение корзины пользователя."""
        return await Basket.filter(user_id=user_id).prefetch_related("menu_item")

    @staticmethod
    async def clear_basket(user_id: UUID):
        """Очистка корзины пользователя."""
        await Basket.filter(user_id=user_id).delete()

    @staticmethod
    async def update_basket_item_quantity(user_id: UUID, menu_item_id: UUID, quantity: int) -> BasketOut:
        """Обновление количества блюда в корзине."""
        try:
            basket = await Basket.get(user_id=user_id, menu_item_id=menu_item_id)
            basket.quantity = quantity
            await basket.save()
            return BasketOut(
                id=basket.id,
                quantity=basket.quantity,
                menu_item_id=basket.menu_item_id,
                user_id=basket.user_id,
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Basket item not found")
