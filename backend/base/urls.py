from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.getUserProfile, name='user_profile'),
    path('users/', views.getUsers, name='users'),
    path('books/', views.getBooks, name='books'),
    path('books/<str:pk>', views.getBook, name='book'),
]