from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('add/', views.addOrderItems, name='order-add'),
    path('myorders/', views.get_my_orders, name='my-orders'),
    path('<str:pk>/', views.getOrderById, name='order-get'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay')
]