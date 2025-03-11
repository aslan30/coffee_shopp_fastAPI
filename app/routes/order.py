from fastapi import APIRouter, HTTPException, Depends, Query
from uuid import UUID
from fastapi_pagination import Page, Params
from app.schemas.order import OrderCreate, OrderOut
from app.services.order import OrderService
from app.utils.security import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/create-from-basket", response_model=OrderOut)
async def create_order_from_basket(
        order_data: OrderCreate,
        current_user: User = Depends(get_current_user),
):
    """
    Создание заказа на основе корзины пользователя.
    """
    return await OrderService.create_order(current_user.id, order_data.dict())


@router.get("/my-orders", response_model=Page[OrderOut])
async def get_my_orders(
        params: Params = Depends(),
        current_user: User = Depends(get_current_user),
):
    """
    Получение всех заказов текущего пользователя с пагинацией.
    """
    return await OrderService.get_user_orders(current_user.id, params)


@router.get("/all-orders", response_model=Page[OrderOut])
async def get_all_orders(
        params: Params = Depends(),
        current_user: User = Depends(get_current_user),
):
    """
    Получение всех заказов (только для администратора) с пагинацией.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view all orders",
        )
    return await OrderService.get_all_orders(params)


@router.get("/ready-orders", response_model=Page[OrderOut])
async def get_ready_orders(
        params: Params = Depends(),
        current_user: User = Depends(get_current_user),
):
    """
    Получение всех готовых заказов для курьера.
    Доступно только для курьеров.
    """
    if current_user.role != RoleEnum.courier:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view ready orders",
        )
    return await OrderService.get_ready_orders(params)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
        order_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """
    Получение деталей заказа по ID.
    Пользователь может получить только свои заказы, админ — все.
    """
    is_admin = current_user.role == RoleEnum.admin
    return await OrderService.get_order_by_id(order_id, current_user.id, is_admin)


@router.post("/{order_id}/ready", response_model=OrderOut)
async def mark_order_as_ready(
        order_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """
    Пометить заказ как готовый (только для администратора).
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to mark orders as ready",
        )
    return await OrderService.mark_order_as_ready(order_id)


@router.post("/{order_id}/accept", response_model=OrderOut)
async def accept_delivery(
        order_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """
    Курьер принимает заказ и меняет статус на 'доставляется'.
    """
    if current_user.role != RoleEnum.courier:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to accept orders",
        )
    return await OrderService.accept_delivery(order_id, current_user.id)


@router.post("/{order_id}/complete", response_model=OrderOut)
async def complete_delivery(
        order_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """
    Курьер завершает доставку и меняет статус на 'доставлено'.
    """
    if current_user.role != RoleEnum.courier:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to complete orders",
        )
    return await OrderService.complete_delivery(order_id, current_user.id)


@router.post("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(
        order_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """
    Отмена заказа. Только пользователь или администратор может отменить заказ.
    """
    is_admin = current_user.role == RoleEnum.admin
    return await OrderService.cancel_order(order_id, current_user.id, is_admin)
