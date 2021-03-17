from django.urls import path
from base.views import book_views as views

urlpatterns = [
    path('', views.getBooks, name='books'),
    path('add/', views.add_book, name='book_add'),
    path('upload/', views.upload_image, name='image_upload'),
    path('<str:pk>/', views.getBook, name='book'),
    path('update/<str:pk>/', views.update_book, name='book_update'),
    path('delete/<str:pk>/', views.delete_book, name='book_delete'),
]
