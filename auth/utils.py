import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from users import services

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_TIME = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_TIME = 60 * 24 * 7  # 7 days
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = services.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(user_id: int):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    payload = {
        'sub': str(user_id),
        'exp': expire_time
    }
    access_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return access_token


def create_refresh_token(user_id: int):
    expire_time = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_TIME)
    payload = {
        'subj': str(user_id),
        'exp': expire_time
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return refresh_token


def decode_jwt_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_aud': False})
        return decoded_token if decoded_token['exp'] >= datetime.utcnow().timestamp() else None
    except:
        return {}
