from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from uuid import UUID

from starlette import status

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services.category import CategoryService
from app.utils.security import get_current_user
from app.models.user import User, RoleEnum
import os
import uuid

router = APIRouter(prefix="/categories", tags=["categories"])

# Папка для хранения изображений категорий
MEDIA_DIR = "media/category_images"
os.makedirs(MEDIA_DIR, exist_ok=True)


async def save_category_image(file: Optional[UploadFile]) -> Optional[str]:
    """Сохраняет изображение категории и возвращает путь к файлу."""
    if not file or not file.filename:
        return None

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(MEDIA_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path


@router.post("/", response_model=CategoryOut)
async def create_category(
        name: str = Form(...),
        image: Optional[UploadFile] = File(None),
        current_user: User = Depends(get_current_user),
):
    """Создание новой категории."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to create categories")

    image_path = await save_category_image(image)

    category_data = CategoryCreate(name=name)
    return await CategoryService.create_category(category_data, image_path)


@router.get("/", response_model=List[CategoryOut])
async def get_all_categories(
        limit: int = Query(default=10, description="Количество категорий на странице", gt=0, le=100),
        offset: int = Query(default=0, description="Смещение для пагинации", ge=0),
        name: Optional[str] = Query(None, description="Фильтр по названию категории"),
):
    """Получение всех категорий с пагинацией и фильтрацией."""
    return await CategoryService.get_all_categories(limit, offset, name)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: UUID):
    """Получение категории по ID."""
    return await CategoryService.get_category_by_id(category_id)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
        category_id: UUID,
        name: Optional[str] = Form(None),
        image: Optional[UploadFile] = File(None),
        delete_image: Optional[bool] = Form(False),
        current_user: User = Depends(get_current_user),
):
    """Обновление категории."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update categories",
        )

    image_path = None
    if image:
        image_path = await save_category_image(image)

    elif delete_image:
        image_path = None

    category_data = CategoryUpdate(name=name)
    return await CategoryService.update_category(category_id, category_data, image_path)


@router.delete("/{category_id}")
async def delete_category(category_id: UUID, current_user: User = Depends(get_current_user)):
    """Удаление категории и всех связанных с ней блюд."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete categories")
    await CategoryService.delete_category(category_id)
    return {"message": "Category and its items deleted"}
