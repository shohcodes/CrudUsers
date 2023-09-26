from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    first_name: str
    username: str

    class Config:
        from_attributes = True


class UserCreateUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    username: str
    password: str


class UserDetailSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    username: str
