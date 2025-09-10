from django.urls import path
from . import views

urlpatterns = [
    # Product Routes
    path('api/products/', views.product_list, name='product_list'),
    path('api/products/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart Routes
    path('api/cart/', views.cart_detail, name='cart_detail'),
    path('api/cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Order Routes
    path('api/orders/', views.create_order, name='create_order'),
    path('api/orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Auth Routes
    path('api/auth/signup/', views.signup, name='signup'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/logout/', views.logout_view, name='logout'),
    path('api/auth/profile/', views.profile, name='profile'),
]

    