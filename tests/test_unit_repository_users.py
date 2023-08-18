import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel, UserDb
from src.repository.users import (
    get_user_by_email,
    confirmed_email,
    create_user,
    update_token,
    update_avatar
)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email_found(self):
        email = 'test@test.test'
        user = User(email=email)
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        email = 'test@test.test'
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=email, db=self.session)
        self.assertIsNone(result)

    async def test_confirmed_email(self):
        get_user_by_email = MagicMock()
        get_user_by_email.return_value = self.user
        result = await confirmed_email(email='test@test.test', db=self.session)
        self.assertTrue(result.confirmed)
    
    async def test_create_user(self):
        body = UserModel(username="username", email="test@test.com", password="password")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "confirmed"))
        self.assertFalse(result.confirmed)
        self.assertTrue(hasattr(result, "avatar"))
        self.assertTrue(hasattr(result, "refresh_token"))

    async def test_update_token(self):
        token = "test"
        result = await update_token(token=token, user=self.user, db=self.session)
        self.assertEqual(result.refresh_token, token)
    
    async def test_update_avatar(self):
        get_user_by_email = MagicMock()
        get_user_by_email.return_value = self.user
        avatar = "test"
        result = await update_avatar('test@test.test', avatar, self.session)
        self.assertEqual(result.avatar, avatar)


if __name__ == '__main__':
    unittest.main()