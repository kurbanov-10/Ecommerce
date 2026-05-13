from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role: str | None = Field(default='user', max_length=50)
    username: str = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(max_length=200)


class UserOut(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
