from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Category
from schemas.Categories import CategoryCreate, CategoryOut
from dependencies import get_current_user
from schemas.users import UserOut

categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.post("/", response_model=CategoryOut)
async def create_category(category_in: CategoryCreate, 
                          db: AsyncSession = Depends(get_db),
                          current_user: UserOut = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi mavjud emas")
    
    new_category = Category(**category_in.model_dump(), user_id=current_user.id)

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@categories_router.get("/{category_id}", response_model=CategoryOut)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category yoq")
    return category


@categories_router.post("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    existing_category = result.scalar_one_or_none()
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category yoq")
    existing_category.name = category.name
    await db.commit()
    await db.refresh(existing_category)
    return existing_category


@categories_router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category yoq")

    await db.delete(category)
    await db.commit()
    return {"detail": "Category o'chirildi"}
