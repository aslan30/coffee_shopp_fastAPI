import logging
from fastapi import APIRouter, Depends
from uuid import UUID
from app.schemas.basket import BasketCreate, BasketUpdate, BasketOut
from app.services.basket import BasketService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/basket", tags=["basket"])


@router.post("/add", response_model=BasketOut)
async def add_to_basket(
        basket_data: BasketCreate,
        current_user: User = Depends(get_current_user),
):
    """Добавление блюда в корзину."""
    return await BasketService.add_to_basket(current_user.id, basket_data.menu_item_id, basket_data.quantity)


@router.delete("/remove/{menu_item_id}")
async def remove_from_basket(
        menu_item_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """Удаление блюда из корзины."""
    await BasketService.remove_from_basket(current_user.id, menu_item_id)
    return {"message": "Item removed from basket"}


@router.get("/", response_model=list[BasketOut])
async def get_basket(current_user: User = Depends(get_current_user)):
    """Получение корзины пользователя."""
    return await BasketService.get_user_basket(current_user.id)


@router.delete("/clear")
async def clear_basket(current_user: User = Depends(get_current_user)):
    """Очистка корзины пользователя."""
    await BasketService.clear_basket(current_user.id)
    return {"message": "Basket cleared"}


logger = logging.getLogger(__name__)


@router.put("/update/{menu_item_id}", response_model=BasketOut)
async def update_basket_item_quantity(
        menu_item_id: UUID,
        basket_data: BasketUpdate,
        current_user: User = Depends(get_current_user),
):
    """Обновление количества блюда в корзине."""
    logger.info(f"Updating basket item for user {current_user.id} with menu item {menu_item_id}")
    return await BasketService.update_basket_item_quantity(
        current_user.id, menu_item_id, basket_data.quantity
    )
