from unittest.mock import MagicMock, patch, AsyncMock
import pytest
from datetime import date, timedelta

from src.database.models import User
from src.services.auth import auth_service

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]

def test_create_contact(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.post(
        "/api/contacts",
        json={"firstname": "test_name",
              "lastname": "test_surname",
              "email": "test@test.com",
              "phone": "test_phone",
              "birthdate": date.today().strftime('%Y-%m-%d')},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["firstname"] == "test_name"
    assert data["lastname"] == "test_surname"
    assert data["email"] == "test@test.com"
    assert data["phone"] == "test_phone"
    assert data["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data

def test_get_contact(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.get(
        "/api/contacts/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["firstname"] == "test_name"
    assert data["lastname"] == "test_surname"
    assert data["email"] == "test@test.com"
    assert data["phone"] == "test_phone"
    assert data["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data

def test_get_contact_not_found(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.get(
        "/api/contacts/2",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"

def test_get_contacts(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.get(
        "/api/contacts",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["firstname"] == "test_name"
    assert data[0]["lastname"] == "test_surname"
    assert data[0]["email"] == "test@test.com"
    assert data[0]["phone"] == "test_phone"
    assert data[0]["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data[0]

def test_get_contacts_with_filter(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    client.post(
        "/api/contacts",
        json={"firstname": "second_name",
              "lastname": "second_surname",
              "email": "second@second.com",
              "phone": "second_phone",
              "birthdate": (date.today()-timedelta(days=1)).strftime('%Y-%m-%d')},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(
        "/api/contacts/?filter=test_name",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["firstname"] == "test_name"
    assert data[0]["lastname"] == "test_surname"
    assert data[0]["email"] == "test@test.com"
    assert data[0]["phone"] == "test_phone"
    assert data[0]["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data[0]

def test_get_contacts_with_birthdays(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.get(
        "/api/contacts/birthdays",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["firstname"] == "test_name"
    assert data[0]["lastname"] == "test_surname"
    assert data[0]["email"] == "test@test.com"
    assert data[0]["phone"] == "test_phone"
    assert data[0]["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data[0]

def test_update_contact(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.put(
        "/api/contacts/1",
        json={"firstname": "test_name2",
                "lastname": "test_surname2",
                "email": "test2@test.com",
                "phone": "test_phone2",
                "birthdate": date.today().strftime('%Y-%m-%d')},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["firstname"] == "test_name2"
    assert data["lastname"] == "test_surname2"
    assert data["email"] == "test2@test.com"
    assert data["phone"] == "test_phone2"
    assert data["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data

def test_update_contact_not_found(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.put(
        "/api/contacts/3",
        json={"firstname": "test_name2",
                "lastname": "test_surname2",
                "email": "test2@test.com",
                "phone": "test_phone2",
                "birthdate": date.today().strftime('%Y-%m-%d')},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"


def test_delete_contact(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.delete(
        "/api/contacts/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["firstname"] == "test_name2"
    assert data["lastname"] == "test_surname2"
    assert data["email"] == "test2@test.com"
    assert data["phone"] == "test_phone2"
    assert data["birthdate"] == date.today().strftime('%Y-%m-%d')
    assert "id" in data


def test_delete_contact_not_found(client, token, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    response = client.delete(
        "/api/contacts/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"