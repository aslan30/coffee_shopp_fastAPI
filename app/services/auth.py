from typing import Optional, List
from fastapi import HTTPException
from starlette import status
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate, UserOut, UserUpdate
from uuid import UUID
from datetime import datetime, timedelta
from app.utils.security import hash_password, generate_verification_code


class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserOut:
        """Создание нового пользователя."""
        existing_user = await User.get_or_none(email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        hashed_password = hash_password(user_data.password)

        user = await User.create(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role or RoleEnum.customer,
            profile_picture=user_data.profile_picture,
        )

        verification_code = generate_verification_code()
        user.verification_code = verification_code

        await user.save()

        return UserOut(**user.__dict__)

    @staticmethod
    async def delete_unverified_users():
        """Удаляет неподтвержденных пользователей старше 2 дней."""
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        await User.filter(is_verified=False, created_at__lte=two_days_ago).delete()

    @staticmethod
    async def delete_user(user_id: UUID):
        """Мягкое удаление пользователя."""
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.is_active = False
        user.deleted_at = datetime.utcnow()
        await user.save()

    @staticmethod
    async def restore_user(user_id: UUID):
        """Восстановление пользователя."""
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.is_active = True
        user.deleted_at = None
        await user.save()

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> UserOut:
        """Получение пользователя по ID."""
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserOut(**user.__dict__)

    @staticmethod
    async def update_user(user_id: UUID, user_data: UserUpdate) -> UserOut:
        """Обновление информации о пользователе."""
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        if user_data.email:
            user.email = user_data.email
        if user_data.profile_picture:
            user.profile_picture = user_data.profile_picture

        if user_data.role:
            if user_data.role == RoleEnum.courier and not user_data.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number is required for couriers",
                )
            user.role = user_data.role

        if user_data.phone:
            user.phone = user_data.phone
        if user_data.additional_phone:
            user.additional_phone = user_data.additional_phone

        await user.save()
        return UserOut(**user.__dict__)

    @staticmethod
    async def search_users(
            email: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            limit: int = 10,
            offset: int = 0,
            sort_by: Optional[str] = None,
            sort_order: Optional[str] = "asc"
    ) -> List[UserOut]:
        """
        Поиск пользователей с пагинацией и сортировкой.

        :param email: Фильтр по email.
        :param first_name: Фильтр по имени.
        :param last_name: Фильтр по фамилии.
        :param limit: Количество пользователей на странице.
        :param offset: Смещение для пагинации.
        :param sort_by: Поле для сортировки (например, "created_at", "first_name").
        :param sort_order: Порядок сортировки ("asc" или "desc").
        :return: Список пользователей.
        """
        if limit < 1 or offset < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid limit or offset value",
            )

        query = User.filter(is_active=True)

        if email:
            query = query.filter(email__icontains=email)
        if first_name:
            query = query.filter(first_name__icontains=first_name)
        if last_name:
            query = query.filter(last_name__icontains=last_name)

        # Сортировка
        if sort_by:
            if sort_order == "desc":
                query = query.order_by(f"-{sort_by}")
            else:
                query = query.order_by(sort_by)

        users = await query.offset(offset).limit(limit).all()
        return [UserOut(**user.__dict__) for user in users]

    @staticmethod
    async def change_user_role(user_id: UUID, new_role: RoleEnum, admin_user: User) -> UserOut:
        """
        Изменение роли пользователя администратором.

        :param user_id: ID пользователя, роль которого нужно изменить.
        :param new_role: Новая роль пользователя.
        :param admin_user: Пользователь, который пытается изменить роль (администратор).
        :return: Обновленный пользователь.
        """
        if admin_user.role != RoleEnum.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin can change user roles",
            )

        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.role = new_role
        await user.save()

        return UserOut(**user.__dict__)
