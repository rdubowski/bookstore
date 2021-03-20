import pytest
from tests.factories import (
    GenreFactory,
    AuthorFactory,
    BookFactory,
    BookFactory,
    ReviewFactory,
    OrderFactory,
    OrderItemFactory,
    ShippingAddressFactory,
    UserFactory,
)
from base.models import (
    Genre,
    Author,
    Book,
    Book,
    Review,
    Order,
    OrderItem,
    ShippingAddress,
)
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_client():
    example_user = UserFactory.build()
    created_user = User.objects.create_user(example_user)
    return created_user


def test_new_user(user_client):
    assert User.objects.count() == 1


def test_genre_factory():
    genre = GenreFactory()
    single_genre_db = Genre.objects.get(name=genre.name)
    assert str(single_genre_db) == genre.name


def test_author_factory():
    author = AuthorFactory()
    single_author_db = Author.objects.get(full_name=author.full_name)
    assert str(single_author_db) == author.full_name


def test_book_factory():
    created_author_1 = AuthorFactory()
    created_author_2 = AuthorFactory()
    created_genre_1 = GenreFactory()
    created_genre_2 = GenreFactory()
    created_genre_3 = GenreFactory()
    book = BookFactory.create(
        author=(created_author_1, created_author_2),
        genre=(created_genre_1, created_genre_2, created_genre_3),
    )
    single_book_db = Book.objects.get(name=book.name)
    assert str(single_book_db) == book.name
    assert single_book_db.author.count() == 2
    assert single_book_db.genre.count() == 3


def test_review_factory():
    review = ReviewFactory()
    single_review_db = Review.objects.get(name=review.name)
    assert str(single_review_db) == review.comment[:50]


def test_order_factory():
    order = OrderFactory()
    single_order_db = Order.objects.get(user=order.user)
    assert str(single_order_db) == str(order.createdAt)


def test_order_item_factory():
    order_item = OrderItemFactory()
    single_order_item_db = OrderItem.objects.get(name=order_item.name)
    assert str(single_order_item_db) == order_item.name


def test_shipping_address_factory():
    shipping_address = ShippingAddressFactory()
    single_shipping_address_db = ShippingAddress.objects.get(
        address=shipping_address.address
    )
    assert str(single_shipping_address_db) == shipping_address.address
