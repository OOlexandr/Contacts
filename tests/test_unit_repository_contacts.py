import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse
from src.repository.contacts import (
    get_contacts,
    get_contact,
    find_contacts,
    find_contacts_by_date,
    create_contact,
    remove_contact,
    update_contact
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_find_contacts(self):
        contacts = [Contact(firstname='test'), Contact(lastname='test'), Contact(email='test'), Contact(phone='test'), Contact()]
        query = 'test'
        self.session.query().filter().filter().all.return_value = contacts[:-1]
        result = await find_contacts(query=query, user=self.user, db=self.session)
        self.assertEqual(result, contacts[:-1])
    
    async def test_find_contacts_by_date(self):
        birthday = date.today()
        birthday += timedelta(days=1)
        contacts = [Contact(birthdate=birthday), Contact()]
        self.session.query().filter().filter().all.return_value = contacts[:-1]
        result = await find_contacts_by_date(user=self.user, db=self.session)
        self.assertEqual(result, contacts[:-1])

    async def test_create_contact(self):
        body = ContactModel(firstname="name", lastname="surname",
                            email="test@test.com", phone='phone',
                            birthdate=date.today())
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthdate, body.birthdate)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(firstname="name", lastname="surname",
                            email="test@test.com", phone='phone',
                            birthdate=date.today())
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(firstname="name", lastname="surname",
                            email="test@test.com", phone='phone',
                            birthdate=date.today())
        self.session.query().filter().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()