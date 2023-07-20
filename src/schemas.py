from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date
import re

class ContactModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    email: str = Field(max_length=25)
    phone: str = Field(max_length=25)
    birthdate: date

class ContactResponse(ContactModel):
    id: int
    
    class Config:
        orm_mode = True