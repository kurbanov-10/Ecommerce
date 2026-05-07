from pydantic import BaseModel, Field


class Tags(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=200)


class TagCreate(Tags):
    pass


class TagOut(Tags):
    id: int
