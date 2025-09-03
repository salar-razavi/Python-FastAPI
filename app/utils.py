from __future__ import annotations
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool
from typing import Final

pwd_context: Final = CryptContext(
    schemes=["bcrypt"],          # می‌تونی بعداً "argon2" رو هم به اول لیست اضافه کنی
    deprecated="auto"
)
#pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password ( password : str)->str:
    return pwd_context.hash(password)
def verify_password(password_input,password_real):
    return pwd_context.verify(password_input,password_real)


async def aget_password_hash(password : str)-> str:
    return await run_in_threadpool(hash_password,password)
async def averfiy_password_hash(plain_password:str , hash_password:str)-> bool:
    return await run_in_threadpool(verify_password,plain_password,hash_password)