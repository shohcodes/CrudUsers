from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import schemas
from auth.utils import authenticate_user, create_access_token, create_refresh_token
from config.dependencies import get_db

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login/')
async def login(credentials: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password or username')
    result = {
        'access_token': create_access_token(user_id=user.id),
        'refresh_token': create_refresh_token(user_id=user.id)
    }
    return result
