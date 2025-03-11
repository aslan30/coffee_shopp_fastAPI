import random
import jwt
from fastapi import HTTPException, status, Depends
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import settings
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

blacklisted_tokens: set[str] = set()


def add_token_to_blacklist(token: str):
    """Добавляет токен в черный список."""
    blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Проверяет, находится ли токен в черном списке."""
    return token in blacklisted_tokens


def hash_password(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    """Декодирует JWT токен."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Возвращает текущего аутентифицированного пользователя."""
    if is_token_blacklisted(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted")

    token_data = decode_access_token(token)
    user = await User.get_or_none(id=token_data.get("sub"))

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or inactive")

    return user


def generate_verification_token(email: str) -> str:
    """Генерирует токен для верификации email."""
    payload = {"email": email, "exp": datetime.utcnow() + timedelta(days=2)}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def authenticate_user(email: str, password: str):
    """Аутентифицирует пользователя."""
    user = await User.get_or_none(email=email)
    if not user or not user.is_verified:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def generate_verification_code(length: int = 4) -> str:
    """Генерирует случайный код верификации."""
    return str(random.randint(10 ** (length - 1), 10 ** length - 1))
