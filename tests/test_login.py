from app.schemas.user import UserAuthToken
from app.oauth2 import verify_access_token
import pytest 

def test_login(client, test_user):
    res = client.post("/login", data={"username":test_user["email"],
                                      "password": test_user["password"]})
    assert res.status_code == 200
    token = UserAuthToken(**res.json())
    assert token.token_type == "bearer"
    token_data = verify_access_token(token.access_token, Exception)
    assert int(token_data.user_id) == test_user["id"] 


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("test_user@gmail.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("test_user@gmail.com", None, 422)])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})

    assert res.status_code == status_code
    

    
