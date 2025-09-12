from django.urls import path
from . import views
from .views import SignupAPIView, LoginAPIView, ProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Products & Categories
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("categories/", views.category_list, name="category-list"),

    # Cart
    path("cart/", views.cart_detail, name="cart-detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="cart-add"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="cart-remove"),

    # Orders
    path("orders/create/", views.create_order, name="order-create"),
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),

    # Auth
    path("auth/signup/", SignupAPIView.as_view(), name="signup"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileAPIView.as_view(), name="profile"),
]
