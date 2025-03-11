from typing import List, Optional
from uuid import UUID
import os
from fastapi import HTTPException, UploadFile
from tortoise.exceptions import DoesNotExist
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut


class CategoryService:
    @staticmethod
    async def create_category(category_data: CategoryCreate, image_path: Optional[str] = None) -> CategoryOut:
        """Создание новой категории."""
        category = await Category.create(
            name=category_data.name,
            image=image_path,
        )
        items = await category.items.all()
        return CategoryOut(
            id=category.id,
            name=category.name,
            image=category.image,
            items=items,
        )

    @staticmethod
    async def get_category_by_id(category_id: UUID) -> CategoryOut:
        """Получение категории по ID."""
        try:
            category = await Category.get(id=category_id).prefetch_related("items")
            items = await category.items.all()
            return CategoryOut(
                id=category.id,
                name=category.name,
                image=category.image,
                items=items,
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")

    @staticmethod
    async def get_all_categories(
            limit: int = 10,
            offset: int = 0,
            name: Optional[str] = None,
    ) -> List[CategoryOut]:
        """
        Получение всех категорий с пагинацией и фильтрацией.

        :param limit: Количество категорий на странице.
        :param offset: Смещение для пагинации.
        :param name: Фильтр по названию категории.
        :return: Список категорий.
        """
        query = Category.all()

        # Фильтрация по названию
        if name:
            query = query.filter(name__icontains=name)

        # Пагинация
        categories = await query.offset(offset).limit(limit).prefetch_related("items")

        result = []
        for category in categories:
            items = await category.items.all()
            result.append(
                CategoryOut(
                    id=category.id,
                    name=category.name,
                    image=category.image,
                    items=items,
                )
            )
        return result

    @staticmethod
    async def update_category(
            category_id: UUID,
            category_data: CategoryUpdate,
            image_path: Optional[str] = None,
    ) -> CategoryOut:
        """Обновление категории."""
        try:
            category = await Category.get(id=category_id)

            if category_data.name is not None:
                category.name = category_data.name

            if image_path is None:
                old_image_path = category.image
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
                category.image = None

            elif image_path:
                old_image_path = category.image
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
                category.image = image_path

            await category.save()
            items = await category.items.all()
            return CategoryOut(
                id=category.id,
                name=category.name,
                image=category.image,
                items=items,
            )
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")

    @staticmethod
    async def delete_category(category_id: UUID):
        """Удаление категории и всех связанных с ней блюд."""
        try:
            category = await Category.get(id=category_id).prefetch_related("items")
            # Удаляем изображение, если оно существует
            if category.image and os.path.exists(category.image):
                os.remove(category.image)
            # Удаляем связанные блюда
            for item in category.items:
                await item.delete()
            # Удаляем категорию
            await category.delete()
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")
