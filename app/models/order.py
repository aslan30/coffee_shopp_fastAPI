from enum import Enum
from uuid import uuid4
from tortoise import fields as f
from tortoise.models import Model


class DeliveryType(str, Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"


class OrderStatus(str, Enum):
    PENDING = "pending"  # Ожидает подтверждения курьером
    ACCEPTED = "accepted"  # Курьер принял заказ
    REJECTED = "rejected"  # Курьер отклонил заказ
    PREPARING = "preparing"  # Заказ готовится
    READY = "ready"  # Заказ готов
    DELIVERING = "delivering"  # Заказ доставляется
    COMPLETED = "completed"  # Заказ доставлен
    CANCELLED = "cancelled"  # Заказ отменен


class Order(Model):
    id = f.UUIDField(pk=True, default=uuid4)
    created_at = f.DatetimeField(auto_now_add=True)
    user = f.ForeignKeyField("models.User", related_name="orders", on_delete=f.CASCADE)
    courier = f.ForeignKeyField("models.User", related_name="assigned_orders", null=True, on_delete=f.SET_NULL)
    phoneNumb1 = f.CharField(max_length=20)
    phoneNumb2 = f.CharField(max_length=20, null=True)
    location = f.CharField(max_length=120, null=True)
    totalPrice = f.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_type = f.CharEnumField(DeliveryType, max_length=10, default=DeliveryType.DELIVERY)
    pickup_location = f.CharField(max_length=120)
    delivery_location = f.CharField(max_length=120)
    status = f.CharEnumField(OrderStatus, max_length=10, default=OrderStatus.PENDING)
    establishment = f.ForeignKeyField("models.Establishment", related_name="orders", null=True, on_delete=f.SET_NULL)
    order_elements = f.ReverseRelation["OrderElement"]

    def __str__(self):
        return f"Order #{self.id}"

    async def update_total_price(self):
        """Обновление общей стоимости заказа."""
        order_elements = await self.order_elements.all().prefetch_related("menu_item")
        total = sum(
            element.quantity * element.menu_item.price
            for element in order_elements
        )
        self.totalPrice = total
        await self.save()
