from sqlalchemy import Integer, Column, String

from config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    phone_number = Column(String(length=9))
    username = Column(String(length=50), unique=True)
    password = Column(String)

    def __str__(self):
        return f'{self.first_name}'
