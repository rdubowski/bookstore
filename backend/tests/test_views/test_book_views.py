import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.urls import reverse
from tests.factories import UserFactory, ReviewFactory, BookFactory, ReviewFactory, GenreFactory, AuthorFactory
from base.models import Book

pytestmark = pytest.mark.django_db

USER_BOOKS_URL = reverse('books')
USER_TOP_BOOKS = reverse('top_books')
ADMIN_ADD_BOOK = reverse('book_add')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = UserFactory.build()
    user.is_staff = True
    user.save()
    return user


def test_user_get_books_2_books(api_client):
    BookFactory()
    BookFactory()
    response = api_client.get(USER_BOOKS_URL)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['pages'] == 1


def test_user_get_books_6_books_1st(api_client):
    books_6 = [BookFactory() for x in range(0, 6)]
    response = api_client.get(USER_BOOKS_URL, {"page": 2})
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['pages'] == 2


def test_user_get_books_6_books_2nd(api_client):
    books_6 = [BookFactory() for x in range(0, 6)]
    response = api_client.get(USER_BOOKS_URL, {"page": 1})
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data['books']) == 4
    assert data['pages'] == 2


def test_user_get_books_with_keyword_found(api_client):
    book = BookFactory()
    response = api_client.get(USER_BOOKS_URL, {"keyword": f"{book.name}"})
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data['books']) == 1


def test_user_get_books_with_keyword_not_found(api_client):
    book = BookFactory()
    response = api_client.get(USER_BOOKS_URL, {"keyword": f"veryrandomkeyowrd"})
    data = json.loads(response.content)
    assert response.status_code == 200
    assert len(data['books']) == 0


def test_user_get_book(api_client):
    book = BookFactory()
    single_book_url = reverse('book', args=(book._id,))
    response = api_client.get(single_book_url)
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data['name'] == book.name
    assert float(data['price']) == float(book.price)


def test_admin_add_book(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.post(ADMIN_ADD_BOOK)
    book = Book.objects.filter(_id=1)
    assert response.status_code == 200
    assert book.exists()


def test_admin_add_many_books(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    api_client.post(ADMIN_ADD_BOOK)
    api_client.post(ADMIN_ADD_BOOK)
    api_client.post(ADMIN_ADD_BOOK)
    books = Book.objects.all()
    assert books.count() == 3


def test_admin_add_book_not_admin(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    response = api_client.post(ADMIN_ADD_BOOK)
    books = Book.objects.all()
    assert response.status_code == 403
    assert books.count() == 0


def test_admin_update_book(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    created_book = BookFactory()
    data = {
        "name": "new name",
        "description": "new description",
        "countInStock": 100,
        "price": 100.50,
        "pagesNum": 100,
        "ISBN": "34324934",
        "author": "new author",
        "genre": "new genre",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_update_book = reverse('book_update', args=(created_book._id,))
    response = api_client.put(url_update_book, data)
    book = Book.objects.get(_id=1)
    author_of_book = book.author.filter(full_name=data['author'])
    genre_of_book = book.genre.filter(name=data['genre'])
    assert response.status_code == 200
    assert book.name == data["name"]
    assert book.description == data["description"]
    assert book.ISBN == data["ISBN"]
    assert book.countInStock == data["countInStock"]
    assert book.pagesNum == data["pagesNum"]
    assert book.price == data["price"]
    assert author_of_book.exists()
    assert genre_of_book.exists()


def test_admin_update_book_multi_author_and_genre(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    created_book = BookFactory()
    data = {
        "name": "new name",
        "description": "new description",
        "countInStock": 100,
        "price": 100.50,
        "pagesNum": 100,
        "ISBN": "34324934",
        "author": "new author, new author2",
        "genre": "new genre, new genre2",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_update_book = reverse('book_update', args=(created_book._id,))
    response = api_client.put(url_update_book, data)
    book = Book.objects.get(_id=1)
    author_of_book = book.author.all()
    genre_of_book = book.genre.all()
    assert response.status_code == 200
    assert author_of_book.count() == 2
    assert genre_of_book.count() == 2


def test_admin_update_book_same_author_and_genre(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    author = AuthorFactory()
    genre = GenreFactory()
    created_book = BookFactory(author=(author,), genre=(genre,))
    created_book_get = Book.objects.get(_id=created_book._id)
    data = {
        "name": "new name",
        "description": "new description",
        "countInStock": 100,
        "price": 100.50,
        "pagesNum": 100,
        "ISBN": "34324934",
        "author": list(created_book_get.author.all()),
        "genre": list(created_book.genre.all()),
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_update_book = reverse('book_update', args=(created_book._id,))
    response = api_client.put(url_update_book, data)
    book = Book.objects.get(_id=1)
    author_of_book = book.author.first().full_name
    genre_of_book = book.genre.first().name
    assert response.status_code == 200
    assert author_of_book == created_book.author.first().full_name
    assert genre_of_book == created_book.genre.first().name


def test_admin_update_book_not_admin(api_client):
    example_user = UserFactory()
    refresh = RefreshToken.for_user(example_user)
    created_book = BookFactory()
    data = {
        "name": "new name",
        "description": "new description",
        "countInStock": 100,
        "price": 100.50,
        "pagesNum": 100,
        "ISBN": "34324934",
        "author": "new author",
        "genre": "new genre",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_update_book = reverse('book_update', args=(created_book._id,))
    response = api_client.put(url_update_book, data)
    assert response.status_code == 403


def test_admin_delete_book(api_client, admin_user):
    book = BookFactory()
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_book_delete = reverse('book_delete', args=(book._id,))
    response = api_client.delete(url_book_delete)
    books = Book.objects.all()
    assert response.status_code == 200
    assert books.count() == 0


def test_admin_delete_book_not_admin(api_client):
    user = UserFactory()
    book = BookFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_book_delete = reverse('book_delete', args=(book._id,))
    response = api_client.delete(url_book_delete)
    books = Book.objects.all()
    assert response.status_code == 403
    assert books.count() == 1


def test_create_book_review(api_client):
    user = UserFactory()
    book = BookFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_create_review = reverse('book_review', args=(book._id,))
    data = {"rating": 5, "comment": "nice comment"}
    response = api_client.post(url_create_review, data)
    data = json.loads(response.content)
    book.refresh_from_db()
    assert response.status_code == 200
    assert data == "Review added"
    assert book.rating == 5


def test_create_book_review_unauth(api_client):
    book = BookFactory()
    url_create_review = reverse('book_review', args=(book._id,))
    data = {"rating": 5, "comment": "nice comment"}
    response = api_client.post(url_create_review, data)
    assert response.status_code == 401


def test_create_book_review_already_exists(api_client):
    user = UserFactory()
    book = BookFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_create_review = reverse('book_review', args=(book._id,))
    data = {"rating": 5, "comment": "nice comment"}
    api_client.post(url_create_review, data)
    response_2 = api_client.post(url_create_review, data)
    data = json.loads(response_2.content)
    book.refresh_from_db()
    assert response_2.status_code == 400
    assert data['detail'] == "Product already reviewed"


# def test_create_book_review_without_rating(api_client):
#     user = UserFactory()
#     book = BookFactory()
#     refresh = RefreshToken.for_user(user)
#     api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
#     url_create_review = reverse('book_review', args=(book._id,))
#     data = {"rating": 0, "comment": "mean comment"}
#     response = api_client.post(url_create_review, data)
#     data = json.loads(response.content)
#     assert response.status_code == 400
#     assert data['detail'] == "Please select a rating"


def test_book_review_rating_average(api_client):
    book = BookFactory()
    user = UserFactory()
    previous_review = ReviewFactory(book=book, rating=3)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    url_create_review = reverse('book_review', args=(book._id,))
    data = {"rating": 5, "comment": "nice comment"}
    response = api_client.post(url_create_review, data)
    data = json.loads(response.content)
    book.refresh_from_db()
    assert response.status_code == 200
    assert data == "Review added"
    assert book.rating == 4


def test_get_top_books(api_client):
    book_1 = BookFactory()
    book_2 = BookFactory()
    book_3 = BookFactory()
    url_create_review_1 = reverse('book_review', args=(book_1._id,))
    url_create_review_2 = reverse('book_review', args=(book_2._id,))
    url_create_review_3 = reverse('book_review', args=(book_3._id,))
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data = {"rating": 5, "comment": "nice comment"}
    post_pos_rating_1 = api_client.post(url_create_review_1, data)
    post_pos_rating_2 = api_client.post(url_create_review_2, data)
    post_pos_rating_3 = api_client.post(url_create_review_3, data)
    response = api_client.get(USER_TOP_BOOKS)
    assert response.status_code == 200
    assert len(response.data) == 3


def test_get_top_book_only_one(api_client):
    book_1 = BookFactory()
    book_2 = BookFactory()
    book_3 = BookFactory()
    url_create_review_1 = reverse('book_review', args=(book_1._id,))
    url_create_review_2 = reverse('book_review', args=(book_2._id,))
    url_create_review_3 = reverse('book_review', args=(book_3._id,))
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    data_pos = {"rating": 5, "comment": "nice comment"}
    data_neg = {"rating": 1, "comment": "mean comment"}
    post_pos_rating_1 = api_client.post(url_create_review_1, data_neg)
    post_pos_rating_2 = api_client.post(url_create_review_2, data_neg)
    post_pos_rating_3 = api_client.post(url_create_review_3, data_pos)
    response = api_client.get(USER_TOP_BOOKS)
    assert response.status_code == 200
    assert len(response.data) == 1