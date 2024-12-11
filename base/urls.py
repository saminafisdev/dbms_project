from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path(
        "category/<int:category_id>/",
        views.product_by_category,
        name="product_by_category",
    ),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("create-order/", views.create_order, name="create_order"),
    path("order-success/", views.order_success, name="order_success"),
]
