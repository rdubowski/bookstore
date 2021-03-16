from django.urls import path
from base.views import book_views as views

urlpatterns = [
    path('', views.getBooks, name='books'),
    path('<str:pk>/', views.getBook, name='book'),
    path('delete/<str:pk>/', views.delete_book, name='book_delete'),
    path('add/', views.add_book, name='book_add')
]
