from app.main import app 
from app import oauth2
from db import schemas , models
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.engine import URL
from app.config import setting
from db.database import get_db
import pytest
from fastapi.testclient import TestClient
import asyncio
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession




TEST_DB_URL = URL.create(
    "postgresql+asyncpg",
    username=setting.username_test,
    password=setting.password_test,
    host=setting.host_test,
    port=setting.port_test,
    database=setting.database_test
)


""" create Engine """
engine = create_async_engine(TEST_DB_URL, echo=False,  poolclass=NullPool)

""" Create Session """
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session", autouse=True)
def prepare_test_db():
    async def _prep():
        async with engine.begin() as conn:
            print("test")
            await conn.run_sync(models.Base.metadata.drop_all)
            await conn.run_sync(models.Base.metadata.create_all)
    asyncio.run(_prep())
    yield
    asyncio.run(engine.dispose())
    
    
    

@pytest.fixture(scope="session")
def client():
    async def override_get_db():
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()    
            except:
                await session.rollback()
                raise
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    


@pytest.fixture(scope="session")
def test_create_user(client):
    user_data = {"email": "u@example.com", "password": "pass"}
    resp = client.post("/users/create", json=user_data)
    assert resp.status_code == 201
    new_user = schemas.Test_User_Out(**resp.json())
    assert new_user.email == "u@example.com"
    new_user.password = user_data['password']
    return new_user
@pytest.fixture(scope="session")
def test_create_user2(client):
    user_data = {"email": "x@example.com", "password": "pass"}
    resp = client.post("/users/create", json=user_data)
    assert resp.status_code == 201
    new_user = schemas.Test_User_Out(**resp.json())
    assert new_user.email == "x@example.com"
    new_user.password = user_data['password']
    return new_user


@pytest.fixture(scope="session")
def token(test_create_user):
    return oauth2.create_access_token({"user_id": test_create_user.id})

@pytest.fixture(scope="session")
def token2(test_create_user2):
    return oauth2.create_access_token({"user_id": test_create_user2.id})

# @pytest.fixture(scope="session")
# def authorized_client(client,token):
#     client.headers = {
#         **client.headers,
#         "Authorization": f"Bearer {token}"
#     }
#     return client

@pytest.fixture(scope="session")
async def test_post(test_create_user):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_create_user.id
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_create_user.id
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_create_user.id
        },
        
    ]
    objs = [models.Post(**post) for post in posts_data]
    async with AsyncSessionLocal() as session:
        session.add_all(objs)
        await session.commit()
        for obj in objs:
            await session.refresh(obj)
    return objs
@pytest.fixture(scope="session")
async def test_post2(test_create_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_create_user2.id
        },       
    ]
    objs = [models.Post(**post) for post in posts_data]
    async with AsyncSessionLocal() as session:
        session.add_all(objs)
        await session.commit()
        for obj in objs:
            await session.refresh(obj)
    return objs
