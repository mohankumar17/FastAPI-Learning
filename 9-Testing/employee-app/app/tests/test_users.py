from app.schemas import Token
from app.config import settings
from jose import jwt
import pytest

def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200

    expected = {
        "status": "App is up and running!!"
    }
    assert res.json() == expected

def test_user_login(test_user, client):
    reqBody = {
        "username": test_user.get("user_email"),
        "password": test_user.get("user_password")
    }
    res = client.post("/login", data = reqBody)
    
    token_res = Token(**res.json())
    decoded_access_token = jwt.decode(token_res.token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])

    user_id = decoded_access_token.get("user_id")

    assert user_id == test_user.get("user_id")
    assert res.status_code == 200

@pytest.mark.parametrize("user_email, user_password, status_code",[
    ("paul@test.com", "abc@999", 401),
    ("tina@test.com", "paul@123", 401),
    (None, "paul@123", 401),
    ("paul@test.com", None, 401),
])
def test_invalid_user_login(client, user_email, user_password, status_code):
    reqBody = {
        "username": user_email,
        "password": user_password
    }
    res = client.post("/login", data = reqBody)
    
    assert res.status_code == status_code