import pytest
from fastapi import HTTPException
from jose import jwt
from app import schemas
from app.config import settings

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') ==  "Hii Buddies, How are you!!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={
        "email" : "sathish123@gmail.com",
        "password" : "password123"
    })
    print(res.json())
    new_user = schemas.Userout(**res.json())
    assert new_user.email == "sathish123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, create_user):
    res = client.post("/login", data={
        "username" : create_user['email'],
        "password" : create_user['password']
    })
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert create_user['id']  == id
    assert login_res.token_type == 'Bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123",  403),
    ("sathish123@gmail.com", "wrongpassword",  403),
    ("wrongemail@gmail.com", "wrongpassword",  403),
    (None, "password123",  422),
    ("wrongemail@gmail.com", None,  422),
])    
def test_incorrect_user(client, create_user, email, password, status_code):
    res = client.post("/login", data={
        "username" : email,
        "password" : password
    })
    print(res)
    print(res.json())
    assert res.status_code == status_code