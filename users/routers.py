from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.bearer import JWTBearer
from auth.utils import hash_password
from config.dependencies import get_db
from users import schemas, services

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[schemas.UserSchema], status_code=200)
async def get_users(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),
                    is_auth=Depends(JWTBearer())):
    users = services.get_users(skip, limit, db)
    return users


@router.post('/', response_model=schemas.UserSchema, status_code=201)
async def create_user(user: schemas.UserCreateUpdateSchema, db: Session = Depends(get_db)):
    model = services.get_user_by_username(db, user.username)
    if model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This username already exists!')
    user.password = hash_password(user.password)
    model = services.create_user(db, user)
    return model


@router.get('/{user_id}', response_model=schemas.UserDetailSchema, )
async def get_user(user_id: int, db: Session = Depends(get_db), is_auth=Depends(JWTBearer())):
    model = services.get_user_by_id(db, user_id)
    if not model:
        raise HTTPException(status_code=404, detail='User not found')
    return model


@router.delete('/{user_id}/', status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db), is_auth=Depends(JWTBearer())):
    model = services.get_user_by_id(db, user_id)
    if not db:
        raise HTTPException(status_code=404, detail='User not found')
    services.delete_user(db, model)
    return {'deleted': True}


@router.put('/{user_id}/', response_model=schemas.UserSchema)
async def update_user(user_id: int, user: schemas.UserCreateUpdateSchema, db: Session = Depends(get_db),
                      is_auth=Depends(JWTBearer())):
    model = services.get_user_by_id(db, user_id)
    if not model:
        raise HTTPException(status_code=404, detail='User not found')
    if user.password:
        user.password = hash_password(user.password)
    model = services.update_user_by_id(db, user, model)
    return model


@router.patch('/{user_id}/', response_model=schemas.UserSchema)
async def partial_update_user(user_id: int, update_data: dict, db: Session = Depends(get_db),
                              is_auth=Depends(JWTBearer())):
    model = services.get_user_by_id(db, user_id)
    if not model:
        raise HTTPException(status_code=404, detail='User not found')
    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])
    model = services.partial_update_user_by_id(db, model, update_data)
    return model
