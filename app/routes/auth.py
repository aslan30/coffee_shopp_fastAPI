import os
import uuid
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query, UploadFile, File
from fastapi.responses import JSONResponse
from uuid import UUID
from starlette import status
from uvicorn.config import logger
from app.schemas.user import UserOut, Token, RegisterResponse, LoginForm
from app.services.auth import UserService
from app.utils.security import (
    get_current_user,
    verify_password,
    create_access_token,
    authenticate_user,
    add_token_to_blacklist,
    oauth2_scheme, generate_verification_code, hash_password, decode_access_token,
)
from app.utils.email import send_verification_email
from app.models.user import User, RoleEnum
from fastapi import Form

router = APIRouter(prefix="/auth", tags=["auth"])

# Папка для хранения изображений профилей
MEDIA_DIR = "media/profile_pictures"

# Создаем папку, если она не существует
os.makedirs(MEDIA_DIR, exist_ok=True)

async def save_profile_picture(file: UploadFile) -> str:

    if not file.filename:
        return None

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(MEDIA_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path

@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Загружает изображение профиля и обновляет путь к нему в базе данных."""
    try:
        # Удаляем старое изображение, если оно существует
        if current_user.profile_picture and os.path.exists(current_user.profile_picture):
            try:
                os.remove(current_user.profile_picture)
            except Exception as e:
                logger.error(f"Failed to delete old profile picture: {str(e)}")

        # Сохраняем новое изображение
        file_path = await save_profile_picture(file)

        # Обновление пути к изображению в базе данных
        current_user.profile_picture = file_path
        await current_user.save()

        return JSONResponse(
            status_code=200,
            content={"message": "Profile picture uploaded successfully", "file_path": file_path}
        )
    except Exception as e:
        logger.error(f"Error during profile picture upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@router.post("/register", response_model=RegisterResponse)
async def register_user(
    background_tasks: BackgroundTasks,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),  # Делаем поле необязательным
):
    try:

        existing_user = await User.get_or_none(email=email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )


        hashed_password = hash_password(password)


        profile_picture_path = None
        if profile_picture and profile_picture.filename:
            profile_picture_path = await save_profile_picture(profile_picture)

        user = await User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role=RoleEnum.customer,
            profile_picture=profile_picture_path,
        )


        verification_code = generate_verification_code()
        user.verification_code = verification_code
        await user.save()

        background_tasks.add_task(send_verification_email, user.email, verification_code)


        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserOut(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                profile_picture=user.profile_picture,
                role=user.role,
            ),
        }
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/verify")
async def verify_email(email: str, code: str):
    """Подтверждение email пользователя."""
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.is_verified = True
    user.verification_code = None
    await user.save()

    return {"message": "Email verified successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: LoginForm = Depends()):
    """Аутентификация пользователя."""
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email to log in",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Возвращает информацию о текущем аутентифицированном пользователе."""
    return UserOut(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        profile_picture=current_user.profile_picture,
        role=current_user.role,
        is_verified=current_user.is_verified,
        is_active=current_user.is_active,
        phone=current_user.phone,
        additional_phone=current_user.additional_phone,
        created_at=current_user.created_at,
    )

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        token_data = decode_access_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        add_token_to_blacklist(token)

        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.get("/search", response_model=List[UserOut])
async def search_users(
    email: Optional[str] = Query(None, description="Фильтр по email"),
    first_name: Optional[str] = Query(None, description="Фильтр по имени"),
    last_name: Optional[str] = Query(None, description="Фильтр по фамилии"),
    limit: int = Query(default=10, description="Количество пользователей на странице (10/20/30)", gt=0, le=30),
    offset: int = Query(default=0, description="Смещение для пагинации", ge=0),
    sort_by: Optional[str] = Query(None, description="Поле для сортировки (например, 'created_at', 'first_name')"),
    sort_order: Optional[str] = Query("asc", description="Порядок сортировки ('asc' или 'desc')"),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to search users",
        )

    users = await UserService.search_users(email, first_name, last_name, limit, offset, sort_by, sort_order)
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, current_user: User = Depends(get_current_user)):
    """Получение информации о пользователе по ID."""
    if current_user.id != user_id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return await UserService.get_user_by_id(user_id)

@router.put("/update-profile", response_model=UserOut)
async def update_user(
    background_tasks: BackgroundTasks,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    confirm_password: Optional[str] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    delete_profile_picture: Optional[bool] = Form(False),
    phone: Optional[str] = Form(None),
    additional_phone: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
):
    try:
        if password and not verify_password(confirm_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password confirmation",
            )

        if first_name is not None:
            current_user.first_name = first_name
        if last_name is not None:
            current_user.last_name = last_name
        if email is not None:
            current_user.email = email
        if password is not None:
            current_user.password = hash_password(password)

        if delete_profile_picture:
            old_profile_picture = current_user.profile_picture
            if old_profile_picture and os.path.exists(old_profile_picture):
                try:
                    os.remove(old_profile_picture)
                except Exception as e:
                    logger.error(f"Failed to delete old profile picture: {str(e)}")
            current_user.profile_picture = None

        if profile_picture and profile_picture.filename:  # Проверяем, что файл передан
            old_profile_picture = current_user.profile_picture
            profile_picture_path = await save_profile_picture(profile_picture)
            current_user.profile_picture = profile_picture_path

            if old_profile_picture and os.path.exists(old_profile_picture):
                try:
                    os.remove(old_profile_picture)
                except Exception as e:
                    logger.error(f"Failed to delete old profile picture: {str(e)}")

        if phone is not None:
            current_user.phone = phone
        if additional_phone is not None:
            current_user.additional_phone = additional_phone

        await current_user.save()

        if email and email != current_user.email:
            verification_code = generate_verification_code()
            current_user.verification_code = verification_code
            await current_user.save()
            background_tasks.add_task(send_verification_email, current_user.email, verification_code)

        return UserOut(**current_user.__dict__)
    except Exception as e:
        logger.error(f"Error during user update: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    password: str = None,
):
    """Удаление пользователя."""
    if current_user.id != user_id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )

    if current_user.id == user_id and not verify_password(password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    await UserService.delete_user(user_id)
    return {"message": "User deleted"}

@router.post("/restore/{user_id}")
async def restore_user(user_id: UUID, current_user: User = Depends(get_current_user)):
    """Восстановление удаленного пользователя."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to restore this user",
        )

    await UserService.restore_user(user_id)
    return {"message": "User restored"}

@router.patch("/users/{user_id}/role", response_model=UserOut)
async def change_user_role(
    user_id: UUID,
    new_role: RoleEnum,
    current_user: User = Depends(get_current_user)
):
    """Изменение роли пользователя."""
    return await UserService.change_user_role(user_id, new_role, current_user)