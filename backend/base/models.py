from django.db import models
from django.contrib.auth.models import User


class Genres(models.Model):
    name = models.CharField(max_length=100, null=False, blank=True)
class Author(models.Model):
    first_name  = models.CharField(max_length=100, null=False, blank=True)
    second_name = models.CharField(max_length=100, null=False, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    # image =
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField(blank=True, null=True)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genres)
    number_of_pages = models.PositiveSmallIntegerField(blank=True)
    ISBN = models.CharField(max_length=20, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)