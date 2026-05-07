import shutil

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from database import get_db
from dependencies import get_current_user
from models import Profile
from schemas.Profiles import ProfileCreate, ProfileOut

profiles_router = APIRouter(prefix="/profiles", tags=["profiles"])


@profiles_router.post('/', response_model=ProfileOut)
async def create_profile(profile_in: ProfileCreate, db=Depends(get_db)):
    profile = await db.scalar(select(Profile).where(Profile.user_id == profile_in.user_id))
    if profile:
        raise HTTPException(status_code=404, detail="Bunday profil mavjud")

    profile_dict = profile_in.model_dump()
    profile = Profile(**profile_dict)

    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return profile


@profiles_router.post('/upload_avatar/')
async def upload_avatar(file: UploadFile = File(...),
                        current_user: ProfileOut = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    from config import UPLOAD_FOLDER

    file_extension = file.filename.split(".")[-1]
    file_location = f"{UPLOAD_FOLDER}/{current_user.id}_avatar.{file_extension}"
    static_location = f"/static/{current_user.id}_avatar.{file_extension}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.user_avatar = static_location
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@profiles_router.post('/{profile_id}', response_model=ProfileOut)
async def update_profile(profile_id: int, profile_in: ProfileCreate, db: Session = Depends(get_db)):
    profile = await db.scalar(select(Profile).where(Profile.id == profile_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profil topilmadi")

    for key, value in profile_in.model_dump().items():
        setattr(profile, key, value)

    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return profile
