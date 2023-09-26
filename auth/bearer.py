from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.utils import decode_jwt_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid auth scheme!")
            if not self.verify_jwt_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token expired or invalid!")
            return decode_jwt_token(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Authorization code is invalid!")

    def verify_jwt_token(self, jwt_token: str) -> bool:
        try:
            payload = decode_jwt_token(jwt_token)
        except:
            payload = None
        return bool(payload)
