
from app.schemas.user import UserResponse

def test_create_user(client):
    email = "test@test.com"
    password = "testpassword"
    res = client.post("/users/", json={"email":email, "password":password})
    new_test_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_test_user.email == email
    assert new_test_user.id == 1

    
def test_get_user(client, test_user):
    res = client.get("/users/{}".format(test_user["id"]))
    assert res.status_code == 200
    user = UserResponse(**res.json())
    assert user.id == test_user["id"]
    assert user.email == test_user["email"]

    
def test_get_nonexistent_user(client):
    res = client.get("/users/99999")
    assert res.status_code == 404
    


