from fastapi import APIRouter , HTTPException , Depends ,status
from db import database , models , schemas
from app import utils , oauth2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authenctication']
)

@router.post("/login",response_model=schemas.Token)
async def login_user(user_login : OAuth2PasswordRequestForm = Depends() , db : AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.email == user_login.username))
    find_user = result.scalars().first()
    if not find_user or not utils.verify_password(user_login.password,find_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential")
    access_token = oauth2.create_access_token({"user_id": find_user.id})
    return {"access_token": access_token, "token_type": "bearer"}