from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    bio: str = Field(default=None, max_length=500)
    location: str = Field(default=None, max_length=100)
    phone_number: str = Field(default=None, max_length=20)
    user_avatar: str = Field(default=None, max_length=200)


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileOut(ProfileBase):
    id: int
    user_id: int
    is_active: bool
