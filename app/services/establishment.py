from uuid import UUID
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from app.models.establishment import Establishment
from app.schemas.establishment import EstablishmentCreate, EstablishmentOut, EstablishmentUpdate


class EstablishmentService:
    @staticmethod
    async def create_establishment(establishment_data: EstablishmentCreate) -> EstablishmentOut:
        """Создание нового заведения."""
        establishment = await Establishment.create(**establishment_data.dict())
        return EstablishmentOut(**establishment.__dict__)

    @staticmethod
    async def get_establishment_by_id(establishment_id: UUID) -> EstablishmentOut:
        """Получение заведения по ID."""
        try:
            establishment = await Establishment.get(id=establishment_id)
            return EstablishmentOut(**establishment.__dict__)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Establishment not found")

    @staticmethod
    async def get_all_establishments() -> list[EstablishmentOut]:
        """Получение всех заведений."""
        establishments = await Establishment.all()
        return [EstablishmentOut(**establishment.__dict__) for establishment in establishments]

    @staticmethod
    async def update_establishment(establishment_id: UUID, establishment_data: EstablishmentUpdate) -> EstablishmentOut:
        """Обновление заведения."""
        try:
            establishment = await Establishment.get(id=establishment_id)
            if establishment_data.location:
                establishment.location = establishment_data.location
            await establishment.save()
            return EstablishmentOut(**establishment.__dict__)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Establishment not found")

    @staticmethod
    async def delete_establishment(establishment_id: UUID):
        """Удаление заведения."""
        try:
            establishment = await Establishment.get(id=establishment_id)
            await establishment.delete()
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Establishment not found")
