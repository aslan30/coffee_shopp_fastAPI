import uuid
from tortoise import fields as f
from tortoise.models import Model
from tortoise.validators import MinValueValidator


class OrderElement(Model):
    id = f.UUIDField(pk=True, default=uuid.uuid4)
    order = f.ForeignKeyField("models.Order", related_name="order_elements", on_delete=f.CASCADE)
    menu_item = f.ForeignKeyField("models.MenuItem", related_name="order_elements", on_delete=f.CASCADE)
    quantity = f.SmallIntField(validators=[MinValueValidator(0)])

    async def save(self, *args, **kwargs):
        """При quantity = 0, удаляем OrderElement вместо сохранения."""
        if self.quantity < 1:
            await self.delete()
        else:
            await super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id}: {self.menu_item.name} x {self.quantity}"
