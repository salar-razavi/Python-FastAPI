from jose import jwt , JWTError
from datetime import datetime , timedelta , timezone
from os import getenv
from db import schemas ,database , models
from fastapi import Depends , HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .config import setting


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(setting.access_token_expire_minutes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str , credentials_exception):
    try:
      payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      id : str = payload.get("user_id")
      if id is None:
          raise credentials_exception
      token_data = schemas.Token_Data(id=id)
    except JWTError :
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    result = await db.execute(select(models.User).where(models.User.id == token_data.id))
    finded_user = result.scalars().first()
    return finded_user