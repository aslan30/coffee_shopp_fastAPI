from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from uuid import UUID
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemOut
from app.services.menu_item import MenuItemService
from app.utils.security import get_current_user
from app.models.user import User, RoleEnum
import os
import uuid

router = APIRouter(prefix="/menu-items", tags=["menu-items"])

MEDIA_DIR = "media/menu_item_images"
os.makedirs(MEDIA_DIR, exist_ok=True)


async def save_menu_item_image(file: Optional[UploadFile]) -> Optional[str]:
    """Сохраняет изображение элемента меню и возвращает путь к файлу."""
    if not file or not file.filename:
        return None

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(MEDIA_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path


@router.post("/", response_model=MenuItemOut)
async def create_menu_item(
        name: str = Form(...),
        description: Optional[str] = Form(None),
        price: float = Form(...),
        category_id: UUID = Form(...),
        image: Optional[UploadFile] = File(None),
        current_user: User = Depends(get_current_user),
):
    """Создание нового элемента меню."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to create menu items")

    image_path = await save_menu_item_image(image)

    menu_item_data = MenuItemCreate(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
    )
    return await MenuItemService.create_menu_item(menu_item_data, image_path)


@router.get("/", response_model=List[MenuItemOut])
async def get_all_menu_items(
        limit: int = Query(default=10, description="Количество элементов меню на странице", gt=0, le=100),
        offset: int = Query(default=0, description="Смещение для пагинации", ge=0),
):
    """Получение всех элементов меню с пагинацией."""
    return await MenuItemService.get_all_menu_items(limit, offset)


@router.get("/most-sold", response_model=List[MenuItemOut])
async def get_most_sold_items(
        limit: int = Query(10, description="Количество товаров"),
        start_date: Optional[str] = Query(None,
                                          description="Начальная дата в формате ISO 8601 (например, 2025-03-10T00:00:00)"),
        end_date: Optional[str] = Query(None,
                                        description="Конечная дата в формате ISO 8601 (например, 2025-03-10T23:59:59)"),
        current_user: User = Depends(get_current_user),
):
    """
    Получение самых продаваемых товаров.
    Доступно только для администратора.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view sales statistics",
        )

    start_date_obj = datetime.fromisoformat(start_date) if start_date else None
    end_date_obj = datetime.fromisoformat(end_date) if end_date else None

    return await MenuItemService.get_most_sold_items(limit, start_date_obj, end_date_obj)


@router.get("/least-sold", response_model=List[MenuItemOut])
async def get_least_sold_items(
        limit: int = Query(10, description="Количество товаров"),
        start_date: Optional[str] = Query(None,
                                          description="Начальная дата в формате ISO 8601 (например, 2025-03-10T00:00:00)"),
        end_date: Optional[str] = Query(None,
                                        description="Конечная дата в формате ISO 8601 (например, 2025-03-10T23:59:59)"),
        current_user: User = Depends(get_current_user),
):
    """
    Получение наименее продаваемых товаров.
    Доступно только для администратора.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view sales statistics",
        )

    start_date_obj = datetime.fromisoformat(start_date) if start_date else None
    end_date_obj = datetime.fromisoformat(end_date) if end_date else None

    return await MenuItemService.get_least_sold_items(limit, start_date_obj, end_date_obj)


@router.get("/most-profitable", response_model=List[MenuItemOut])
async def get_most_profitable_items(
        limit: int = Query(10, description="Количество товаров"),
        start_date: Optional[str] = Query(None,
                                          description="Начальная дата в формате ISO 8601 (например, 2025-03-10T00:00:00)"),
        end_date: Optional[str] = Query(None,
                                        description="Конечная дата в формате ISO 8601 (например, 2025-03-10T23:59:59)"),
        current_user: User = Depends(get_current_user),
):
    """
    Получение самых прибыльных товаров.
    Доступно только для администратора.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view sales statistics",
        )

    start_date_obj = datetime.fromisoformat(start_date) if start_date else None
    end_date_obj = datetime.fromisoformat(end_date) if end_date else None

    return await MenuItemService.get_most_profitable_items(limit, start_date_obj, end_date_obj)


@router.get("/least-profitable", response_model=List[MenuItemOut])
async def get_least_profitable_items(
        limit: int = Query(10, description="Количество товаров"),
        start_date: Optional[str] = Query(None,
                                          description="Начальная дата в формате ISO 8601 (например, 2025-03-10T00:00:00)"),
        end_date: Optional[str] = Query(None,
                                        description="Конечная дата в формате ISO 8601 (например, 2025-03-10T23:59:59)"),
        current_user: User = Depends(get_current_user),
):
    """
    Получение наименее прибыльных товаров.
    Доступно только для администратора.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view sales statistics",
        )

    start_date_obj = datetime.fromisoformat(start_date) if start_date else None
    end_date_obj = datetime.fromisoformat(end_date) if end_date else None

    return await MenuItemService.get_least_profitable_items(limit, start_date_obj, end_date_obj)


@router.get("/category/{category_id}", response_model=List[MenuItemOut])
async def get_menu_items_by_category(
        category_id: UUID,
        limit: int = Query(default=10, description="Количество элементов меню на странице", gt=0, le=100),
        offset: int = Query(default=0, description="Смещение для пагинации", ge=0),
        current_user: User = Depends(get_current_user),
):
    """Получение всех элементов меню выбранной категории с пагинацией."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to view this data")
    return await MenuItemService.get_menu_items_by_category(category_id, limit, offset)


@router.get("/{menu_item_id}", response_model=MenuItemOut)
async def get_menu_item(menu_item_id: UUID):
    """Получение элемента меню по ID."""
    return await MenuItemService.get_menu_item_by_id(menu_item_id)


@router.put("/{menu_item_id}", response_model=MenuItemOut)
async def update_menu_item(
    menu_item_id: UUID,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_id: Optional[UUID] = Form(None),
    image: Optional[UploadFile] = File(None),
    delete_image: Optional[bool] = Form(False),
    current_user: User = Depends(get_current_user),
):
    """Обновление элемента меню."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to update menu items")

    image_path = None
    if image:
        image_path = await save_menu_item_image(image)

    elif delete_image:
        image_path = None

    menu_item_data = MenuItemUpdate(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
    )
    return await MenuItemService.update_menu_item(menu_item_id, menu_item_data, image_path)


@router.delete("/{menu_item_id}")
async def delete_menu_item(menu_item_id: UUID, current_user: User = Depends(get_current_user)):
    """Удаление элемента меню."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete menu items")
    await MenuItemService.delete_menu_item(menu_item_id)
    return {"message": "Menu item deleted"}


@router.delete("/category/{category_id}")
async def delete_menu_items_by_category(category_id: UUID, current_user: User = Depends(get_current_user)):
    """Удаление всех блюд выбранной категории."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to delete menu items")
    await MenuItemService.delete_menu_items_by_category(category_id)
    return {"message": "All menu items in the category deleted"}
