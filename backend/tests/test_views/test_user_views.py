import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
import json
from tests.factories import UserFactory

pytestmark = pytest.mark.django_db

REGISTER_URL = reverse("register")
USER_PROFILE_URL = reverse("user_profile")
USER_PROFILE_UPDATE_URL = reverse("update_user_profile")
ADMIN_GET_USERS = reverse("users")


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    user = UserFactory.build()
    user.is_staff = True
    user.save()
    return user

def test_register_request(api_client):
    data = {
        "name": "Example User",
        "email": "email@email.com",
        "password": "test_pass_123",
    }
    response = api_client.post(REGISTER_URL, data)
    assert response.status_code == 200


def test_register_request_reapeted(api_client):
    data = {
        "name": "Example User",
        "email": "email@email.com",
        "password": "test_pass_123",
    }
    response = api_client.post(REGISTER_URL, data)
    response2 = api_client.post(REGISTER_URL, data)
    assert response2.status_code == 400


def test_update_user_profile_without_password(api_client):
    user = UserFactory.build()
    user.password = make_password("xyz1234656")
    user.save()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data = {
        "email": "email@email.com",
        "name": "custom_name",
        "password": "",
    }
    response = api_client.put(USER_PROFILE_UPDATE_URL, data)
    assert response.status_code == 200
    assert User.objects.filter(first_name=data["name"]).exists()
    assert User.objects.filter(email=data["email"]).exists()
    assert user.check_password("xyz1234656")


def test_update_user_profile_with_password(api_client):
    user = UserFactory.build()
    user.password = make_password("xyz1234656")
    user.save()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data = {
        "email": user.email,
        "name": user.username,
        "password": "testpass123",
    }
    response = api_client.put(USER_PROFILE_UPDATE_URL, data)
    user.refresh_from_db()
    assert response.status_code == 200
    assert User.objects.filter(first_name=data["name"]).exists()
    assert User.objects.filter(email=data["email"]).exists()
    assert user.check_password(data["password"])


def test_user_profile(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(USER_PROFILE_URL)
    assert response.status_code == 200


def test_user_profile_unauth(api_client):
    user = UserFactory()
    response = api_client.get(USER_PROFILE_URL)
    assert response.status_code == 401


def test_admin_get_users(api_client, admin_user):
    UserFactory()
    UserFactory()
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(ADMIN_GET_USERS)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data) == 3


def test_admin_get_users_not_admin(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(ADMIN_GET_USERS)
    assert response.status_code == 403


def test_admin_get_user_by_id(api_client, admin_user):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_get_user_by_id = reverse('user', args=(example_user.id,))
    response = api_client.get(url_get_user_by_id)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data["username"] == example_user.username
    assert not data["isAdmin"]


def test_admin_get_user_by_id_not_admin(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    example_user = UserFactory()
    url_get_user_by_id = reverse('user', args=(example_user.id,))
    response = api_client.get(url_get_user_by_id)
    assert response.status_code == 403


def test_admin_update_user(api_client, admin_user):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_get_user_by_id = reverse('update_user', args=(example_user.id,))
    data = {
        "name": "name_example",
        "email": "email@example.com",
        "isAdmin": True,
    }
    response = api_client.put(url_get_user_by_id, data)
    example_user.refresh_from_db()
    assert response.status_code == 200
    assert data["email"] == example_user.email
    assert data["isAdmin"]
    assert data["name"] == example_user.first_name


def test_admin_update_user_not_admin(api_client, admin_user):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(example_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_get_user_by_id = reverse('update_user', args=(example_user.id,))
    data = {
        "name": "name_example",
        "email": "email@example.com",
        "isAdmin": True,
    }
    response = api_client.put(url_get_user_by_id, data)
    assert response.status_code == 403


def test_admin_delete_user(api_client, admin_user):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_get_user_by_id = reverse('delete_user', args=(example_user.id,))
    response = api_client.delete(url_get_user_by_id)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data == "User was deleted"


def test_admin_delete_user_not_admin(api_client):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(example_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_get_user_by_id = reverse('delete_user', args=(example_user.id,))
    response = api_client.delete(url_get_user_by_id)
    assert response.status_code == 403