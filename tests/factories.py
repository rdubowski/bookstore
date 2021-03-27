from django.contrib.auth.models import User
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
import factory
from factory import Faker
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    password = Faker(
        "password",
        length=42,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.fuzzy.FuzzyText()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    full_name = factory.fuzzy.FuzzyText()


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    user = factory.SubFactory(UserFactory)
    author = factory.SubFactory(AuthorFactory)
    genre = factory.SubFactory(GenreFactory)
    name = factory.fuzzy.FuzzyText()
    price = factory.fuzzy.FuzzyDecimal(5, 100)
    countInStock = factory.fuzzy.FuzzyInteger(20, 100)
    pagesNum = factory.fuzzy.FuzzyInteger(50, 400)

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for auth in extracted:
                self.author.add(auth)

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for gen in extracted:
                self.genre.add(gen)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)
    name = factory.fuzzy.FuzzyText()
    rating = factory.fuzzy.FuzzyInteger(1, 5)
    comment = factory.fuzzy.FuzzyText()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    paymentMethod = factory.fuzzy.FuzzyText()
    taxPrice = factory.fuzzy.FuzzyDecimal(1, 50)
    shippingPrice = factory.fuzzy.FuzzyDecimal(1, 50)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    book = factory.SubFactory(BookFactory)
    name = factory.fuzzy.FuzzyText()
    order = factory.SubFactory(OrderFactory)
    price = factory.fuzzy.FuzzyDecimal(5, 100)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)


class ShippingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    order = factory.SubFactory(OrderFactory)
    address = factory.fuzzy.FuzzyText()
    city = factory.fuzzy.FuzzyText()
    postalCode = factory.fuzzy.FuzzyText()
    country = factory.fuzzy.FuzzyText()
