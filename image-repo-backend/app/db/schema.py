from typing import List, Optional

from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str
    is_public: bool
    class Config:
        orm_mode = True


class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    token: str
    images: List[Image] = []

    class Config:
        orm_mode = True