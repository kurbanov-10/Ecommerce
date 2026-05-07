import security

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from models import User
from schemas.users import UserCreate, UserOut, Token
from dependencies import role_checker

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post('/', response_model=UserOut)
async def create_user(bg_tasks: BackgroundTasks, user_in: UserCreate, db: Session = Depends(get_db)):
    user = await db.scalar(select(User).where(User.username == user_in.username))
    if user:
        raise HTTPException(status_code=404, detail="Bunday foydalanuvchi mavjud")

    user_dict = user_in.model_dump()
    hashed_password = security.get_password_hash(user_dict.pop("password"))

    user = User(**user_dict, hashed_password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # bg_tasks.add_task(send_welcome_email, f"{user.username}@gmail.com")

    return user


@users_router.post('/login/', response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await db.scalar(select(User).where(User.username == form.username))
    if not user:
        raise HTTPException(status_code=404, detail="Bunday foydalanuvchi mavjud emas")

    if not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Username yoki parol noto'g'ri")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post('/{user_id}', response_model=UserOut)
async def update_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db),
                      _: UserOut = Depends(role_checker("admin"))):
    existing_user = await db.scalar(select(User).where(User.id == user_id))
    if not existing_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    for key, value in user_in.model_dump().items():
        if key == "password":
            setattr(existing_user, "hashed_password", security.get_password_hash(value))
        else:
            setattr(existing_user, key, value)

    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)

    return existing_user
