import uuid
from tortoise import fields as f
from tortoise.models import Model


class Establishment(Model):
    id = f.UUIDField(primary_key=True, default=uuid.uuid4)
    location = f.CharField(max_length=50)

    def __str__(self):
        return f"Establishment(id={self.id}, location={self.location})"
