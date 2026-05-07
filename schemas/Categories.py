from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
