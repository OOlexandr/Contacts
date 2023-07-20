from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import date

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(filter: str = None, db: Session = Depends(get_db)):
    if filter is None:
        contacts = await repository_contacts.get_contacts(db)
        return contacts
    contacts = await repository_contacts.find_contacts(filter, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts

@router.get("/birthdays", response_model=List[ContactResponse])
async def read_birthdays(db: Session=Depends(get_db)):
    contacts = await repository_contacts.find_contacts_by_date(db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact