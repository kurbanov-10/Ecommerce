from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Product
from schemas.Products import ProductCreate, ProductOut
from dependencies import get_current_user
from schemas.users import UserOut

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.post("/", response_model=ProductOut)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db),
                         user_id: UserOut = Depends(get_current_user)):
    if not user_id:
        raise HTTPException(status_code=400, detail=f"{user_id} idli user mavjud emas")

    new_product = Product(**product_in.model_dump().values(), user_id=user_id)

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@products_router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product yoq")
    return product


@products_router.post("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    existing_product = result.scalar_one_or_none()
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product yoq")

    existing_product.name = product.name
    existing_product.price = product.price
    await db.commit()
    await db.refresh(existing_product)
    return existing_product


@products_router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product yoq")

    await db.delete(product)
    await db.commit()
    return {"detail": "Product o'chirildi"}
