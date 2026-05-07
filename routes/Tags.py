from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Tag
from schemas.Tags import TagCreate, TagOut
from dependencies import get_current_user
from schemas.users import UserOut

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.post("/", response_model=TagOut)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db),
                     user: UserOut = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=400, detail="User topilmadi")

    new_tag = Tag(**tag.model_dump().values(), user_id=user.id)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


@tags_router.get("/{tag_id}", response_model=TagOut)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag topilmadi")
    return tag


@tags_router.post("/{tag_id}", response_model=TagOut)
async def update_tag(tag_id: int, tag: TagCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    existing_tag = result.scalar_one_or_none()
    if existing_tag is None:
        raise HTTPException(status_code=404, detail="Tag topilmadi")

    existing_tag.name = tag.name
    await db.commit()
    await db.refresh(existing_tag)
    return existing_tag


@tags_router.delete("/{tag_id}")
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag topilmadi")

    await db.delete(tag)
    await db.commit()
    return {"detail": "Tag o'chirildi"}
