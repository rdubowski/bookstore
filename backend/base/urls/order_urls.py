from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('', views.get_orders, name='orders'),
    path('add/', views.addOrderItems, name='order-add'),
    path('myorders/', views.get_my_orders, name='my-orders'),
    path('<str:pk>/', views.getOrderById, name='order-get'),
    path('<str:pk>/deliver/', views.update_order_to_delivered, name='deliver'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),

]
