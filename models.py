from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Float, String, Integer, Boolean, ForeignKey, Table

from database import Base
from enums import Roles


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    first_name: Mapped[str] = mapped_column(String(length=100))
    last_name: Mapped[str] = mapped_column(String(length=100))
    hashed_password: Mapped[str] = mapped_column(String(length=200))
    role: Mapped[Roles] = mapped_column(String(length=50), default=Roles.USER, nullable=True)
    
    profile: Mapped['Profile'] = relationship(back_populates='user', cascade='all, delete-orphan')
    categories: Mapped[list['Category']] = relationship(back_populates="user")


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bio: Mapped[str] = mapped_column(String(length=500), nullable=True)
    location: Mapped[str] = mapped_column(String(length=100), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(length=20), nullable=True)
    user_avatar: Mapped[str] = mapped_column(String(length=200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='profile')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), unique=True)
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user: Mapped['User'] = relationship(back_populates='categories')

    products: Mapped[list['Product']] = relationship(back_populates='category', cascade='all, delete-orphan')


product_tags = Table(
    'product_tags',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100))
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='products')
    tags: Mapped[list['Tag']] = relationship(back_populates='products', secondary=product_tags)


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)
    products: Mapped[list['Product']] = relationship(back_populates='tags', secondary=product_tags)