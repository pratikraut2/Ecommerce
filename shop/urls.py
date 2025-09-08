from . import views
from django.urls import path

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
   path('cart/', views.cart_detail, name='cart_detail'),
   path('checkout/', views.checkout, name='checkout'),
   path('order/<int:order_id>/', views.order_detail, name='order_detail'),

   path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/profile/', views.profile, name='profile'),
]