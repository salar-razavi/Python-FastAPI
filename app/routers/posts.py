
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from sqlalchemy import func
from db import database , models , schemas
from app import oauth2
from typing import Optional



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


""" Show All Posts """
@router.get("/",response_model=list[schemas.Show_Posts2])
async def posts(db : AsyncSession = Depends(database.get_db), current_user = Depends(oauth2.get_current_user),limit: int = None,search:Optional[str]=""):
    result = await db.execute(select(models.Post).where(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit))
    all_posts = result.scalars().all()
    result = await db.execute(select(models.Post,func.count(models.Vote.post_id).label("vote_count")).outerjoin(models.Vote,models.Post.id == models.Vote.post_id).group_by(models.Post.id).where(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit))
    votes = result.mappings().all()
    if not votes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"You don't have any post")
    return votes
""" ------------------------------------------------------------------------------------------ """


""" Create Post """
@router.post("/create",status_code=status.HTTP_201_CREATED,response_model=schemas.Show_Posts)
async def posts(post : schemas.PostCreate, db : AsyncSession = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post
""" ------------------------------------------------------------------------------------------ """



""" Find Post By ID """
@router.get("/{id}",response_model=schemas.Show_Posts2)
async def one_post(id : int, db : AsyncSession = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    result = await db.execute(select(models.Post,func.count(models.Vote.post_id).label("vote_count")).outerjoin(models.Vote,models.Post.id == models.Vote.post_id).group_by(models.Post.id).where((models.Post.id == id),(models.Post.owner_id == current_user.id)))
    finded_post = result.mappings().first()
    if not finded_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id = {id} Not Found")
    
    return finded_post
""" ------------------------------------------------------------------------------------------ """



""" Delete Post By ID """

@router.delete("/{id}",response_model=schemas.Show_Posts)
async def delete_post (id : int , db : AsyncSession = Depends(database.get_db), current_user  = Depends(oauth2.get_current_user)):
    result = await db.execute(select(models.Post).where(models.Post.id == id))
    deleted_post = result.scalars().first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id = {id} Not Found")
    if  deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    await db.delete(deleted_post)
    await db.commit()
    
    return deleted_post
""" ------------------------------------------------------------------------------------------ """



""" Update Post By ID """
@router.put("/{id}",response_model=schemas.Show_Posts,status_code=status.HTTP_202_ACCEPTED)
async def updated_post (id : int , post : schemas.Update_Post , db : AsyncSession = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    result = await db.execute(select(models.Post).where(models.Post.id == id))
    updated_post = result.scalars().first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id = {id} Not Found")
    if updated_post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    for key , value in post.model_dump(exclude_unset=True).items():
        setattr (updated_post , key, value)
    await db.commit()
    await db.refresh(updated_post)
    return updated_post
    
""" ------------------------------------------------------------------------------------------ """