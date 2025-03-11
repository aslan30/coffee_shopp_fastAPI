import os
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from starlette import status
from tortoise import functions
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException
from tortoise.functions import Sum
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.order_element import OrderElement
from app.schemas.menu_item import MenuItemOut, MenuItemUpdate, MenuItemCreate


class MenuItemService:
    @staticmethod
    async def create_menu_item(menu_item_data: MenuItemCreate, image_path: Optional[str] = None) -> MenuItemOut:
        """Создание нового элемента меню."""
        menu_item = await MenuItem.create(
            name=menu_item_data.name,
            description=menu_item_data.description,
            price=menu_item_data.price,
            category_id=menu_item_data.category_id,
            image=image_path,
        )
        return MenuItemOut(**menu_item.__dict__)

    @staticmethod
    async def get_menu_items_by_category(
            category_id: UUID,
            limit: int = 10,
            offset: int = 0,
    ) -> List[MenuItemOut]:
        """Получение всех элементов меню выбранной категории с пагинацией."""
        try:
            # Проверка существования категории
            await Category.get(id=category_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")

        menu_items = await MenuItem.filter(category_id=category_id).offset(offset).limit(limit).all()
        return [MenuItemOut(**menu_item.__dict__) for menu_item in menu_items]

    @staticmethod
    async def get_menu_item_by_id(menu_item_id: UUID) -> MenuItemOut:
        """Получение элемента меню по ID."""
        try:
            menu_item = await MenuItem.get(id=menu_item_id)
            return MenuItemOut(**menu_item.__dict__)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Menu item not found")

    @staticmethod
    async def get_all_menu_items(limit: int = 10, offset: int = 0) -> List[MenuItemOut]:
        """Получение всех элементов меню с пагинацией."""
        menu_items = await MenuItem.all().offset(offset).limit(limit)
        return [MenuItemOut(**menu_item.__dict__) for menu_item in menu_items]

    @staticmethod
    async def update_menu_item(
            menu_item_id: UUID,
            menu_item_data: MenuItemUpdate,
            image_path: Optional[str] = None,
    ) -> MenuItemOut:
        """Обновление элемента меню."""
        try:
            menu_item = await MenuItem.get(id=menu_item_id)

            if menu_item_data.name is not None:
                menu_item.name = menu_item_data.name
            if menu_item_data.description is not None:
                menu_item.description = menu_item_data.description
            if menu_item_data.price is not None:
                menu_item.price = menu_item_data.price
            if menu_item_data.category_id is not None:
                category = await Category.get_or_none(id=menu_item_data.category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Category not found",
                    )
                menu_item.category_id = menu_item_data.category_id

            if image_path is None:
                old_image_path = menu_item.image
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
                menu_item.image = None

            elif image_path:
                old_image_path = menu_item.image
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception:
                        pass
                menu_item.image = image_path

            await menu_item.save()
            return MenuItemOut(**menu_item.__dict__)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Menu item not found")

    @staticmethod
    async def delete_menu_item(menu_item_id: UUID):
        """Удаление элемента меню."""
        try:
            menu_item = await MenuItem.get(id=menu_item_id)
            # Удаляем изображение, если оно существует
            if menu_item.image and os.path.exists(menu_item.image):
                os.remove(menu_item.image)
            await menu_item.delete()
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Menu item not found")

    @staticmethod
    async def delete_menu_items_by_category(category_id: UUID):
        """Удаление всех блюд выбранной категории."""
        menu_items = await MenuItem.filter(category_id=category_id)
        for menu_item in menu_items:
            if menu_item.image and os.path.exists(menu_item.image):
                os.remove(menu_item.image)
        await MenuItem.filter(category_id=category_id).delete()

    @staticmethod
    async def get_most_sold_items(limit: int, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[
        MenuItemOut]:
        """Получение самых продаваемых товаров."""
        filters = {}
        if start_date:
            filters["order__created_at__gte"] = start_date
        if end_date:
            filters["order__created_at__lte"] = end_date

        query = OrderElement.annotate(total_sold=functions.Sum('quantity')).filter(**filters).group_by(
            'menu_item_id').order_by('-total_sold').limit(limit)

        most_sold_items = await query.values('menu_item_id', 'total_sold')
        return [MenuItemOut.from_orm(await MenuItem.get(id=item['menu_item_id'])) for item in most_sold_items]

    @staticmethod
    async def get_least_sold_items(limit: int, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[
        MenuItemOut]:
        """Получение наименее продаваемых товаров."""
        filters = {}
        if start_date:
            filters["order__created_at__gte"] = start_date
        if end_date:
            filters["order__created_at__lte"] = end_date

        query = OrderElement.annotate(total_sold=functions.Sum('quantity')).filter(**filters).group_by(
            'menu_item_id').order_by('total_sold').limit(limit)

        least_sold_items = await query.values('menu_item_id', 'total_sold')
        return [MenuItemOut.from_orm(await MenuItem.get(id=item['menu_item_id'])) for item in least_sold_items]

    @staticmethod
    async def get_most_profitable_items(
            limit: int, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> List[MenuItemOut]:
        """Получение самых прибыльных товаров."""
        filters = {}
        if start_date:
            filters["order__created_at__gte"] = start_date
        if end_date:
            filters["order__created_at__lte"] = end_date

        query = (
            OrderElement.annotate(total_sold=Sum("quantity"))
            .filter(**filters)
            .group_by("menu_item_id")
            .limit(limit)
        )

        items = await query.values("menu_item_id", "total_sold")

        profitable_items = []
        for item in items:
            menu_item = await MenuItem.get(id=item["menu_item_id"])
            total_profit = item["total_sold"] * menu_item.price
            profitable_items.append((menu_item, total_profit))

        profitable_items.sort(key=lambda x: x[1], reverse=True)

        return [MenuItemOut.from_orm(item[0]) for item in profitable_items[:limit]]

    @staticmethod
    async def get_least_profitable_items(
            limit: int, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> List[MenuItemOut]:
        """Получение наименее прибыльных товаров."""
        filters = {}
        if start_date:
            filters["order__created_at__gte"] = start_date
        if end_date:
            filters["order__created_at__lte"] = end_date

        query = (
            OrderElement.annotate(total_sold=Sum("quantity"))
            .filter(**filters)
            .group_by("menu_item_id")
            .limit(limit)
        )

        items = await query.values("menu_item_id", "total_sold")

        profitable_items = []
        for item in items:
            menu_item = await MenuItem.get(id=item["menu_item_id"])
            total_profit = item["total_sold"] * menu_item.price
            profitable_items.append((menu_item, total_profit))

        profitable_items.sort(key=lambda x: x[1])

        return [MenuItemOut.from_orm(item[0]) for item in profitable_items[:limit]]
