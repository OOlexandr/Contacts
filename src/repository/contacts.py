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
                                    Contact.email==query, Contact.phone==query)).all()


def is_anniversary_soon(month, day, n: int):
    """
    Finds if the anniversary is within n days from current date

    :param month: The month of the anniversary.
    :type user: Extract
    :param day: The day of the anniversary.
    :type day: Extract
    :param n: The number of days.
    :type db: int
    :return: Is the anniversary is in the given time period.
    :rtype: bool
    """
    today = date.today()
    days_in_month = {
            1: 31,
            2: 28,  # Ignoring leap years
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31}
    this_month = (month == today.month)
    next_month = (month == today.month+1) | (month==1 and today.month==12)
    day_this_month = (day >= today.day) & (day <= today.day + n)
    day_next_month = (today.day - days_in_month[today.month] + n) >= day
    return (this_month & day_this_month) | (next_month & day_next_month)


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
    return db.query(Contact).filter(Contact.user_id == user.id).\
            filter(is_anniversary_soon(extract('month', Contact.birthdate),\
                                       extract('day', Contact.birthdate), 7)).all()

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