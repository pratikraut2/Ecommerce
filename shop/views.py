# views.py
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer, UserSerializer
)

User = get_user_model()


# ---------- Public Product / Category ----------

@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    qs = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return Response(ProductSerializer(product, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    qs = Category.objects.all()
    return Response(CategorySerializer(qs, many=True).data)


# ---------- Cart ----------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return Response(CartSerializer(cart).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    qty = int(request.data.get("quantity", 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return Response({"detail": "removed"}, status=status.HTTP_200_OK)


# ---------- Orders ----------

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    shipping_address = request.data.get("shipping_address", "")
    payment_method = request.data.get("payment_method", "COD")
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return Response({"detail": "Cart empty"}, status=status.HTTP_400_BAD_REQUEST)

    total = cart.total_price()
    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        payment_method=payment_method,
        total_amount=Decimal(total),
        payment_status="Pending",
    )
    for ci in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=ci.product,
            quantity=ci.quantity,
            unit_price=ci.product.price,
        )
    cart.items.all().delete()
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return Response(OrderSerializer(order).data)


# ---------- Auth: Signup, Login, Profile ----------

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email", "")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username & password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username & password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
