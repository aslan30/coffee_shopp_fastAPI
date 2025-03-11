import uuid
from tortoise import fields as f
from tortoise.models import Model


class Basket(Model):
    id = f.UUIDField(pk=True, default=uuid.uuid4)
    quantity = f.SmallIntField(default=0)
    menu_item = f.ForeignKeyField("models.MenuItem", related_name="basket", on_delete=f.CASCADE)
    user = f.ForeignKeyField("models.User", related_name="basket", on_delete=f.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.menu_item}-{self.quantity}"
