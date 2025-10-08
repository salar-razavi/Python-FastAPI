from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import database , models , schemas
from ..utils import hash_password , averfiy_password_hash , aget_password_hash


router = APIRouter(
    prefix="/users",
    tags=['Users']
)



""" Create User"""
@router.post("/create",response_model=schemas.User_Out,status_code=status.HTTP_201_CREATED)
async def create_user(user : schemas.User_Create,db : AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email Already Exist")
    
    created_user = models.User(
        email=user.email,
        password= await aget_password_hash(user.password)
    )
                               
    db.add(created_user)
    await db.commit()
    await db.refresh(created_user)
    return created_user
""" ------------------------------------------------------------------------------------------ """





""" Get All User"""
@router.get("/",response_model=list[schemas.User_Out])
async def get_all_user(db : AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User))
    all_user = result.scalars().all()
    return all_user
    
""" ------------------------------------------------------------------------------------------ """



""" Get User By ID"""
@router.get("/{id}",response_model=schemas.User_Out)
async def get_user_id(id : int,db : AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == id))
    finded_user = result.scalars().first()
    if not finded_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User With ID = {id} Not Found")
    return finded_user
    
""" ------------------------------------------------------------------------------------------ """


""" Update User By ID """
@router.put("/{id}",response_model=schemas.User_Out,status_code=status.HTTP_202_ACCEPTED)
async def updated_user (id : int , user : schemas.User_Update , db : AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == id))
    updated_user = result.scalars().first()
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id = {id} Not Found")
    for key , value in user.model_dump(exclude_unset=True).items():
        setattr (updated_user , key, await aget_password_hash(value))
    await db.commit()
    await db.refresh(updated_user)
    return updated_user
    
""" ------------------------------------------------------------------------------------------ """