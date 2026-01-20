from django.urls import path

from . import views


app_name = "store"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.register, name="register"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
]

