from django.urls import path
from base.views import orders_views as views

urlpatterns = [
    path('add/', views.addOrderItems, name='order-add'),
    path('<str:pk>/', views.getOrderById, name='order-get')
]
