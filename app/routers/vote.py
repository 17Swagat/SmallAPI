from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import utils, schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.get('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(get_db), 
         current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    
    if vote.dir == 1:
        # Vote
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'Post with id: {vote.post_id} has already been voted by {current_user.id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return JSONResponse(status_code=status.HTTP_201_CREATED, 
                            content={'message': 'Vote Added Successfully'})
    
    elif vote.dir == 0:
        # Un-Vote
        if vote_found:
            vote_query.delete(synchronize_session = False)
            db.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, 
                                content={'message': 'Vote Deleted Successfully'})
        elif vote_found is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'Post with id : {vote.post_id} has no votes by ')
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid value for dir, must be 0 or 1")