from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(filter: str = None, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    if filter is None:
        contacts = await repository_contacts.get_contacts(current_user, db)
        return contacts
    contacts = await repository_contacts.find_contacts(filter, current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts

@router.get("/birthdays", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_birthdays(db: Session=Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.find_contacts_by_date(current_user, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)

@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact