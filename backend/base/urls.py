from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRouter, name='routes'),
    path('books/', views.getBooks, name='books'),
    path('books/<str:pk>', views.getBook, name='book')
]