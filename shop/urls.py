from django.urls import path
from . import views
from .views import SignupView, LoginView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # products & categories
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("categories/", views.category_list, name="category-list"),

    # cart
    path("cart/", views.cart_detail, name="cart-detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="cart-add"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="cart-remove"),

    # orders
    path("orders/create/", views.create_order, name="order-create"),
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),
    path("orders/<int:order_id>/pay/", views.order_pay, name="order-pay"),

    # stripe webhook (public)
    path("stripe/webhook/", views.stripe_webhook, name="stripe-webhook"),

    # auth
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    
]
