from db import database , models , schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status , HTTPException , Depends , APIRouter
from .. import oauth2


router = APIRouter (
    prefix="/votes",
    tags=['votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def votes(vote: schemas.Vote, db : AsyncSession = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    result = await db.execute(select(models.Post).where(models.Post.id == vote.post_id))
    if not result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not found")
    result = await db.execute(select(models.Vote).where((models.Vote.post_id == vote.post_id),(models.Vote.user_id == current_user.id)))
    finded_vote = result.scalars().first()
    if vote.dir == 1 :
        if finded_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="you can not vote the specefic post twice")
        new_vote = models.Vote(
            post_id=vote.post_id ,
            user_id = current_user.id 
        )
        db.add(new_vote)
        await db.commit()
        await db.refresh(new_vote)
        return {"you voted successfully"}
    await db.delete(finded_vote)
    await db.commit()
    return{"your vote is deleted successfully"}
    
    