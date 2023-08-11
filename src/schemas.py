from pydantic import BaseModel, Field, EmailStr
from datetime import date
import re

class ContactModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    email: EmailStr
    phone: str = Field(max_length=25)
    birthdate: date

class ContactResponse(ContactModel):
    id: int
    
    class Config:
        orm_mode = True

class UserModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)

class UserDb(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr