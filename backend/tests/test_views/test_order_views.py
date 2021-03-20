import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.urls import reverse
from tests.factories import OrderFactory, UserFactory, BookFactory, ShippingFactory
from base.models import Order



pytestmark = pytest.mark.django_db

# USER_BOOKS_URL = reverse('orders')
# USER_TOP_BOOKS = reverse('top_books')
# ADMIN_ADD_BOOK = reverse('book_add')

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = UserFactory.build()
    user.is_staff = True
    user.save()
    return user
