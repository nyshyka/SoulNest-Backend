from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserLogin, UserPublic
from app.utils.security import create_access_token, hash_password, verify_password
from .deps import get_current_user


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> UserPublic:
    if not payload.email or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required.")

    existing_user = await db.execute(select(User).where(User.email == payload.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered.")

    user = User(
        name=payload.name or payload.email.split("@")[0],
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_guest=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    if not payload.email or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required.")

    query = await db.execute(select(User).where(User.email == payload.email))
    user = query.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    token = create_access_token(subject=user.id)
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)


@router.post("/guest", response_model=Token, status_code=status.HTTP_201_CREATED)
async def guest(db: AsyncSession = Depends(get_db)) -> Token:
    guest_email = "guest@example.com"
    result = await db.execute(select(User).where(User.email == guest_email))
    guest_user = result.scalar_one_or_none()

    if guest_user is None:
        guest_user = User(
            name="Guest",
            email=guest_email,
            password_hash=hash_password("guest"),
            is_guest=True,
        )
        db.add(guest_user)
        await db.commit()
        await db.refresh(guest_user)

    token = create_access_token(subject=guest_user.id)
    return Token(access_token=token)
