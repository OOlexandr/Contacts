from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
import sqlalchemy as sa


from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session) -> List[Contact]:
    return db.query(Contact).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def find_contacts(query: str, db: Session) ->List[Contact]:
    return db.query(Contact).filter(sa.or_(Contact.firstname==query, Contact.lastname==query,
                                    Contact.email==query, Contact.phone==query))


def age_years_at(sa_col, next_days: int = 0):
    stmt = sa.func.age(
        (sa_col - sa.func.cast(timedelta(next_days), sa.Interval))
        if next_days != 0
        else sa_col
    )
    stmt = sa.func.date_part("year", stmt)
    return stmt

def is_anniversary_soon(anniversary: date, n: int):
    return age_years_at(anniversary, n) > age_years_at(anniversary)

async def find_contacts_by_date(db: Session) ->List[Contact]:
    return db.query(Contact).filter(is_anniversary_soon(Contact.birthdate, 7))

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email,
                      phone=body.phone, birthdate=body.birthdate)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthdate = body.birthdate
        db.commit()
    return contact