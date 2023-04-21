import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username='TestAdmin',
        email='admin@example.com',
        first_name='Admin',
        last_name='Adminksiy',
        password='12345',
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        email='maks@example.com',
        first_name='Maks',
        last_name='Alekseev',
        password='12345',
    )


@pytest.fixture
def token_admin(admin):
    token = AccessToken.for_user(admin)
    return {
        'access': str(token),
    }


@pytest.fixture
def admin_client(token_admin):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_admin["access"]}')
    return client


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_user["access"]}')
    return client
