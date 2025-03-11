from uuid import UUID
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from fastapi_pagination import Page, Params, paginate

from app.models.basket import Basket
from app.models.establishment import Establishment
from app.models.order import DeliveryType, Order, OrderStatus
from app.models.order_element import OrderElement
from app.models.user import User, RoleEnum
from app.schemas.order import OrderOut


class OrderService:
    @staticmethod
    async def create_order(user_id: UUID, order_data: dict):
        """
        Создание нового заказа на основе корзины пользователя.
        """
        try:
            user = await User.get(id=user_id)
            basket_items = await Basket.filter(user_id=user_id).prefetch_related("menu_item")
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

        if not basket_items:
            raise HTTPException(status_code=400, detail="Basket is empty")

        delivery_type = order_data.get("delivery_type")
        if delivery_type not in [DeliveryType.DELIVERY, DeliveryType.PICKUP]:
            raise HTTPException(status_code=400, detail="Invalid delivery type")

        establishment = None
        if delivery_type == DeliveryType.PICKUP:
            establishment_id = order_data.get("establishment_id")
            if not establishment_id:
                raise HTTPException(status_code=400, detail="Establishment ID is required for pickup")
            try:
                establishment = await Establishment.get(id=establishment_id)
            except DoesNotExist:
                raise HTTPException(status_code=404, detail="Establishment not found")

        courier = None
        if delivery_type == DeliveryType.DELIVERY:
            courier = await User.filter(role=RoleEnum.courier, is_active=True).first()
            if not courier:
                raise HTTPException(status_code=400, detail="No available couriers")

        order = await Order.create(
            user=user,
            courier=courier,
            phoneNumb1=order_data["phoneNumb1"],
            phoneNumb2=order_data.get("phoneNumb2"),
            pickup_location=order_data["pickup_location"],
            delivery_location=order_data["delivery_location"],
            delivery_type=delivery_type,
            status=OrderStatus.PENDING,
            establishment=establishment,
        )

        for basket_item in basket_items:
            await OrderElement.create(
                order=order,
                menu_item=basket_item.menu_item,
                quantity=basket_item.quantity,
            )

        await order.update_total_price()

        await Basket.filter(user_id=user_id).delete()

        if delivery_type == DeliveryType.DELIVERY:
            await OrderService.notify_courier(order.id, courier.id)

        return order

    @staticmethod
    async def get_user_orders(user_id: UUID, params: Params) -> Page[OrderOut]:
        """
        Получение всех заказов текущего пользователя с пагинацией.
        """
        orders = await Order.filter(user_id=user_id).order_by("-created_at")
        return paginate(orders, params)

    @staticmethod
    async def get_all_orders(params: Params) -> Page[OrderOut]:
        """
        Получение всех заказов (только для администратора) с пагинацией.
        """
        orders = await Order.all().order_by("-created_at")
        return paginate(orders, params)

    @staticmethod
    async def get_order_by_id(order_id: UUID, user_id: UUID, is_admin: bool = False) -> OrderOut:
        """
        Получение заказа по ID. Пользователь может получить только свои заказы, админ — все.
        """
        order = await Order.get_or_none(id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if not is_admin and order.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to view this order")
        return order

    @staticmethod
    async def mark_order_as_ready(order_id: UUID):
        """
        Пометить заказ как готовый (только для администратора).
        """
        order = await Order.get_or_none(id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = OrderStatus.READY
        await order.save()
        return order

    @staticmethod
    async def get_ready_orders(params: Params) -> Page[OrderOut]:
        """
        Получение всех готовых заказов для курьера (только для доставки).
        """

        orders = await Order.filter(
            status=OrderStatus.READY,
            delivery_type=DeliveryType.DELIVERY
        ).order_by("-created_at").all()

        return paginate(orders, params)

    @staticmethod
    async def accept_delivery(order_id: UUID, courier_id: UUID):
        """
        Курьер принимает заказ и меняет статус на 'доставляется'.
        """
        order = await Order.get_or_none(id=order_id, status=OrderStatus.READY)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or not ready")
        order.courier_id = courier_id
        order.status = OrderStatus.DELIVERING
        await order.save()
        return order

    @staticmethod
    async def complete_delivery(order_id: UUID, courier_id: UUID):
        """
        Курьер завершает доставку и меняет статус на 'доставлено'.
        """
        order = await Order.get_or_none(id=order_id, courier_id=courier_id, status=OrderStatus.DELIVERING)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or not delivering")
        order.status = OrderStatus.COMPLETED
        await order.save()
        return order

    @staticmethod
    async def cancel_order(order_id: UUID, user_id: UUID, is_admin: bool = False):
        """
        Отмена заказа. Только пользователь или администратор может отменить заказ.
        """
        order = await Order.get_or_none(id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if not is_admin and order.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to cancel this order")
        if order.status not in [OrderStatus.PENDING, OrderStatus.ACCEPTED]:
            raise HTTPException(status_code=400, detail="Order cannot be cancelled")
        order.status = OrderStatus.CANCELLED
        await order.save()
        return order

    @staticmethod
    async def notify_courier(order_id: UUID, courier_id: UUID):
        """
        Отправка уведомления курьеру.
        """
        print(f"Уведомление отправлено курьеру {courier_id} о заказе {order_id}")

    @staticmethod
    async def notify_admin(order: Order):
        """
        Уведомление администратора об отмене заказа.
        """
        admin_users = await User.filter(role=RoleEnum.admin).all()
        for admin in admin_users:
            print(f"Уведомление администратору {admin.id}: Заказ {order.id} отменен пользователем {order.user_id}.")
