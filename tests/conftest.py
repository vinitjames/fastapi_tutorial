from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import db_config
from app import models
from app.oauth2 import create_access_token
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user import UserAuthTokenData
from app.schemas.post import PostCreate

SQL_TEST_DATABASE_URI = f'postgresql://{db_config.postgres_username}:{db_config.postgres_password}@{db_config.postgres_hostname}:{db_config.postgres_port}/{db_config.postgres_dbname}_test'


test_engine = create_engine(SQL_TEST_DATABASE_URI)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture
def client():
    models.base.metadata.drop_all(bind=test_engine)
    models.base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(client):
    user_cred = {"email": "test_user@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_cred)
    assert res.status_code == 201
    user_data = res.json()
    user_data.update({"password": user_cred["password"]})
    return user_data
    

@pytest.fixture
def token(client, test_user):
    return create_access_token(UserAuthTokenData(user_id = test_user["id"]))
    
@pytest.fixture
def authenticated_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def create_posts(test_user):
    posts = [{"title": "1st Post", "content": "1st Post Content"},
             {"title": "2nd Post", "content": "2nd Post Content"},
             {"title": "3rd Post", "content": "3rd Post Content"},
             {"title": "4th Post", "content": "4th Post Content"}]
    post_entry = [models.Post(**post, owner_id = test_user["id"]) for post in posts]    
    db = override_get_db
    db.add_all(posts_entry)
    db.commit()
    return db.query(models.Post).all()
    
    
