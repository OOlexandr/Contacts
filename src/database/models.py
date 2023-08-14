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
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref='contacts')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    confirmed = Column(Boolean, default=False)
    email = Column(String(250), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)