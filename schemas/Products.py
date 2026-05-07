from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
