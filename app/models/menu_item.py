import uuid
from tortoise import fields as f
from tortoise.models import Model


class MenuItem(Model):
    id = f.UUIDField(pk=True, default=uuid.uuid4)
    name = f.CharField(unique=True, max_length=100)
    image = f.CharField(max_length=255, null=True)
    description = f.TextField(null=True)
    price = f.FloatField(null=True)
    category = f.ForeignKeyField("models.Category", related_name="items", null=True, on_delete="CASCADE")

    def __str__(self):
        return f"{self.name} ({self.id})"
