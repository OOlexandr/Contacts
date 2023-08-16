from typing import List
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
import sqlalchemy as sa


from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user.

    :param user: The user to retrieve notes for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()

async def find_contacts(query: str, user: User, db: Session) ->List[Contact]:
    """
    Retrieves a list of contacts for a specific user with a substring in a firstname, lastname, email or phone.

    :param query: The substring used for query.
    :type query: str
    :param user: The user to retrieve notes for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).filter(sa.or_(Contact.firstname==query, Contact.lastname==query,
                                    Contact.email==query, Contact.phone==query))


def age_years_at(date, next_days: int = 0):
    """
    Finds number of full years passed since date after a number of days

    :param date: The date.
    :type date: date
    :param next_days: The number of days.
    :type next_days: int
    :return: The number of full years.
    :rtype: int
    """
    stmt = sa.func.age(
        (date - sa.func.cast(timedelta(next_days), sa.Interval))
        if next_days != 0
        else date
    )
    stmt = sa.func.date_part("year", stmt)
    return stmt

def is_anniversary_soon(anniversary: date, n: int):
    """
    Finds if the anniversary is within n days from current date

    :param anniversary: The anniversary to check.
    :type user: date
    :param n: The number of days.
    :type db: int
    :return: Is the anniversary is in the given time period.
    :rtype: bool
    """
    return age_years_at(anniversary, n) > age_years_at(anniversary)

async def find_contacts_by_date(user: User, db: Session) ->List[Contact]:
    """
    Retrieves a list of contacts for a specific user with a birthdate within 7 days from current date.

    :param user: The user to retrieve notes for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).filter(is_anniversary_soon(Contact.birthdate, 7))

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(firstname=body.firstname, lastname=body.lastname, email=body.email,
                      phone=body.phone, birthdate=body.birthdate, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.id == contact_id).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthdate = body.birthdate
        db.commit()
    return contact