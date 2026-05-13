import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app

load_dotenv()

DATABASE_URL = os.getenv("TEST_DATABASE_URL")


test_engine = create_async_engine(DATABASE_URL,
                                  connect_args={'check_same_thread': False},
                                  echo=True)

TestSession = async_sessionmaker(bind=test_engine, autoflush=False)


async def override_get_db():
    async with TestSession() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


test_client = TestClient(app)

def test_create_user():
    response = test_client.post("/users", json={"username": "admin",
                                                "password": "testpassword",
                                                "first_name": "Test",
                                                "last_name": "User",
                                                "role": "customer"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    
    
def test_create_profile():
    token = test_client.post("/users/login/",
                             data={"username": "admin", "password": "testpassword"}).json()["access_token"]
    response = test_client.post("/profiles",
                                headers={"Authorization": f"Bearer {token}"},
                                json={"bio": "Test profile", "location": "Uzbekistan","phone_number": "998995447020", "is_active": True, "user_avatar":"djsbdwnkl.jpg", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Test profile"
    assert data["location"] == "Uzbekistan"
    assert data["phone_number"] == "998995447020"
    assert data["is_active"] is True
    assert data["user_avatar"] == "djsbdwnkl.jpg"
    assert data["user_id"] == 1


def test_create_category():
    token = test_client.post("/users/login/",
                             data={"username": "admin", "password": "testpassword"}).json()["access_token"]
    response = test_client.post("/categories/",
                                headers={"Authorization": f"Bearer {token}"},
                                json={"name": "Test Category",
                                      "description": "A category for testing"})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "A category for testing"
    
 