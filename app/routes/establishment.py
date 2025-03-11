from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from app.schemas.establishment import EstablishmentCreate, EstablishmentUpdate, EstablishmentOut
from app.services.establishment import EstablishmentService
from app.utils.security import get_current_user
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/establishments", tags=["establishments"])


@router.post("/", response_model=EstablishmentOut)
async def create_establishment(
        establishment_data: EstablishmentCreate,
        current_user: User = Depends(get_current_user),
):
    """Создание нового заведения."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to create establishments")
    return await EstablishmentService.create_establishment(establishment_data)


@router.get("/", response_model=list[EstablishmentOut])
async def get_all_establishments():
    """Получение всех заведений."""
    return await EstablishmentService.get_all_establishments()


@router.get("/{establishment_id}", response_model=EstablishmentOut)
async def get_establishment(establishment_id: UUID):
    """Получение заведения по ID."""
    return await EstablishmentService.get_establishment_by_id(establishment_id)


@router.put("/{establishment_id}", response_model=EstablishmentOut)
async def update_establishment(
        establishment_id: UUID,
        establishment_data: EstablishmentUpdate,
        current_user: User = Depends(get_current_user),
):
    """Обновление заведения."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to update establishments")
    return await EstablishmentService.update_establishment(establishment_id, establishment_data)


@router.delete("/{establishment_id}")
async def delete_establishment(
        establishment_id: UUID,
        current_user: User = Depends(get_current_user),
):
    """Удаление заведения."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete establishments")
    await EstablishmentService.delete_establishment(establishment_id)
    return {"message": "Establishment deleted"}
