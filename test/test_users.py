from .utils import *
from fastapi import status
from ..models import Todos
from ..routers.users import get_db, get_current_user
from ..routers.auth import bcrypt_context

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["username"] == "monuv"
    assert response.json()[0]['email'] == "dailycrunches@gmail.com"
    assert response.json()[0]['first_name'] == "monu"
    assert response.json()[0]['last_name'] == "verma"
    assert response.json()[0]['role'] == "admin"
    assert response.json()[0]['phone_number'] == "12345890"


def test_change_password_success(test_user):
    response = client.put("/user/change_pass",json={"password": "testpassword",
                                                 "new_password":"newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT



def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_pass",json={"password": "wrong_password",
                                                 "new_password":"newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}




def test_update_phone_number_success(test_user):
    response = client.put("user/update_phoneNo/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT



