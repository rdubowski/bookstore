import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.urls import reverse
from tests.factories import (
    OrderFactory,
    UserFactory,
    BookFactory,
    ShippingAddressFactory,
)
from base.models import Order

pytestmark = pytest.mark.django_db

USER_ADD_ORDER = reverse("order_add")
USER_MY_ORDERS = reverse("my_orders")
ADMIN_ALL_ORDERS = reverse("orders")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = UserFactory.build()
    user.is_staff = True
    user.save()
    return user


def test_user_add_order_items_no_items_auth(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data = {
        "orderItems": [],
        "paymentMethod": "",
        "taxPrice": 0,
        "shippingPrice": 0,
        "totalPrice": 0,
        "shippingAddress": {
            "address": "",
            "city": "",
            "postalCode": "",
            "country": "",
        },
    }
    response = api_client.post(USER_ADD_ORDER, data=data, format="json")
    data = json.loads(response.content)
    orders = Order.objects.all()
    assert response.status_code == 400
    assert data["detail"] == "No order Items"
    assert orders.count() == 0


def test_user_add_order_items_auth(api_client):
    user = UserFactory()
    book_1 = BookFactory()
    count_of_book_1_before = book_1.countInStock
    book_2 = BookFactory()
    count_of_book_2_before = book_2.countInStock
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data_to_send = {
        "orderItems": [
            {"book": book_1._id, "qty": 1, "price": book_1.price},
            {"book": book_2._id, "qty": 1, "price": book_2.price},
        ],
        "paymentMethod": "card",
        "taxPrice": 10,
        "shippingPrice": 10,
        "totalPrice": 20 + book_1.price + book_2.price,
        "shippingAddress": {
            "address": "street",
            "city": "example_city",
            "postalCode": "00-000",
            "country": "Poland",
        },
    }
    response = api_client.post(
        USER_ADD_ORDER, data=data_to_send, format="json"
    )
    orders = Order.objects.all()
    book_1.refresh_from_db()
    book_2.refresh_from_db()
    assert response.status_code == 200
    assert book_1.countInStock == count_of_book_1_before - 1
    assert book_2.countInStock == count_of_book_2_before - 1
    assert orders.count() == 1


def test_user_add_order_items_not_auth(api_client):
    response = api_client.post(USER_ADD_ORDER, {})
    orders = Order.objects.all()
    assert response.status_code == 401
    assert orders.count() == 0


def test_user_get_orders_auth(api_client):
    user = UserFactory()
    order_1 = OrderFactory(user=user)
    order_2 = OrderFactory(user=user)
    order_3_not_by_user = OrderFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(USER_MY_ORDERS)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data) == 2


def test_user_get_orders_unauth(api_client):
    response = api_client.get(USER_MY_ORDERS)
    assert response.status_code == 401


def test_user_get_order_auth(api_client):
    user = UserFactory()
    order = OrderFactory(user=user)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_single_order = reverse("order_get", args=(order._id,))
    response = api_client.get(url_single_order)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data["paymentMethod"] == order.paymentMethod


def test_user_get_not_his_order_auth(api_client):
    user_order_owner = UserFactory()
    user_without_order = UserFactory()
    order = OrderFactory(user=user_order_owner)
    refresh = RefreshToken.for_user(user_without_order)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_single_order = reverse("order_get", args=(order._id,))
    response = api_client.get(url_single_order)
    data = json.loads(response.content)
    assert response.status_code == 400
    assert data["detail"] == "Not authorized to view this order"


def test_user_get_not_existing_order(api_client):
    user = UserFactory()
    order_id = Order.objects.all().count() + 2
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_single_order = reverse("order_get", args=(order_id,))
    response = api_client.get(url_single_order)
    data = json.loads(response.content)
    assert response.status_code == 400
    assert data["detail"] == "Order does not exists"


def test_admin_get_order_auth(admin_user, api_client):
    user = UserFactory()
    order = OrderFactory(user=user)
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_single_order = reverse("order_get", args=(order._id,))
    response = api_client.get(url_single_order)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data["paymentMethod"] == order.paymentMethod


def test_user_get_order_unauth(api_client):
    order = OrderFactory()
    url_single_order = reverse("order_get", args=(order._id,))
    response = api_client.get(url_single_order)
    assert response.status_code == 401


def test_user_order_to_paid_auth(api_client):
    user = UserFactory()
    order = OrderFactory(user=user)
    order_before_payment_isPaid = order.isPaid
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_pay_order = reverse("pay", args=(order._id,))
    response = api_client.put(url_pay_order)
    data = json.loads(response.content)
    order_after_paid = Order.objects.get(_id=order._id)
    assert response.status_code == 200
    assert data == "Order was paid"
    assert not order_before_payment_isPaid
    assert order_after_paid.isPaid


def test_user_order_to_paid_unauth(api_client):
    order = OrderFactory()
    url_pay_order = reverse("pay", args=(order._id,))
    order_not_changed = Order.objects.get(_id=order._id)
    response = api_client.put(url_pay_order)
    assert response.status_code == 401
    assert not order_not_changed.isPaid


def test_admin_get_orders_auth(api_client, admin_user):
    user_1 = UserFactory()
    user_2 = UserFactory()
    order_1 = OrderFactory(user=user_1)
    order_2 = OrderFactory(user=user_2)
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(ADMIN_ALL_ORDERS)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data) == 2


def test_admin_get_orders_not_admin(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.get(ADMIN_ALL_ORDERS)
    assert response.status_code == 403


def test_admin_update_to_delivered_auth(api_client, admin_user):
    order = OrderFactory()
    order_before_deliver_isDelivered = order.isDelivered
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_deliver_order = reverse("deliver", args=(order._id,))
    response = api_client.put(url_deliver_order)
    data = json.loads(response.content)
    order_after_deliver = Order.objects.get(_id=order._id)
    assert response.status_code == 200
    assert data == "Order was delivered"
    assert not order_before_deliver_isDelivered
    assert order_after_deliver.isDelivered


def test_admin_update_to_delivered_not_admin(api_client):
    order = OrderFactory()
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_deliver_order = reverse("deliver", args=(order._id,))
    response = api_client.put(url_deliver_order)
    take_order = Order.objects.get(_id=order._id)
    assert response.status_code == 403
    assert not take_order.isDelivered
