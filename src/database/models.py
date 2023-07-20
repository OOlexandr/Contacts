from sqlalchemy import Column, Integer, String, Boolean, func, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False)
    email = Column(String(25))
    phone = Column(String(25))
    birthdate = Column(Date)