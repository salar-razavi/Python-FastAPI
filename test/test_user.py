from db import schemas
import pytest
from jose import jwt
from app.config import setting



def test_login_user(client,test_create_user):
    response = client.post("/login", data={"username": test_create_user.email, "password": test_create_user.password})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token,setting.secret_key,algorithms=[setting.algorithm])
    id : str = payload.get("user_id")
    assert test_create_user.id == id
    assert response.status_code == 200
    return login_res
    
    
    
@pytest.mark.parametrize("email,password,status_code,details",[
    ('wrongemail@gamil.com','wrongpassword',403,'Invalid Credential Or Email Not Found'),
    ('wrongemail@gamil.com',None,403,'Invalid Credential Or Email Not Found'),
    (None,'wrongpassword',403,'Invalid Credential Or Email Not Found')
])
def test_incorrect_login(client,email,password,status_code,details):
    response = client.post("/login",data={"username":email,"password":password})
    assert (response.status_code == status_code or response.status_code == 420)
    assert response.json().get('detail') == details