from django.contrib import admin

from .models import (
    Author,
    Book,
    Genre,
    Order,
    OrderItem,
    Review,
    ShippingAddress,
)

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Genre)
admin.site.register(Author)
