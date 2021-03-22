from django.urls import path

from base.views import book_views as views

urlpatterns = [
    path("", views.get_books, name="books"),
    path("add/", views.add_book, name="book_add"),
    path("author/<str:pk>/", views.get_books_by_auth, name="book_by_auth"),
    path("upload/", views.upload_image, name="image_upload"),
    path("<str:pk>/reviews/", views.create_book_review, name="book_review"),
    path("top/", views.get_top_books, name="top_books"),
    path("<str:pk>/", views.get_book, name="book"),
    path("update/<str:pk>/", views.update_book, name="book_update"),
    path("delete/<str:pk>/", views.delete_book, name="book_delete"),
]
