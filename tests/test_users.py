from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import db_config
from app import models
from app.schemas.user import UserResponse
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    


def test_create_user(client):
    email = "test@test.com"
    password = "testpassword"
    res = client.post("/users/", json={"email":email, "password":password})
    new_test_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_test_user.email == email
    assert new_test_user.id == 1

