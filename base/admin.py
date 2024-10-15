from django.contrib import admin
from .models import (
    Customer,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Address,
)

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
