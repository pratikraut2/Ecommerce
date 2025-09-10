from django.shortcuts import render
import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import stripe

from django.contrib.auth import get_user_model
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, UserSerializer

User = get_user_model()
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")


# ---------- Public product/category ----------
@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    qs = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk, is_active=True)
    return Response(ProductSerializer(p, context={"request": request}).data)


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
    # create order
    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        payment_method=payment_method,
        total_amount=Decimal(total),
        payment_status="Pending",
    )
    # copy items
    for ci in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=ci.product,
            quantity=ci.quantity,
            unit_price=ci.product.price,
        )
    # clear cart items
    cart.items.all().delete()
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return Response(OrderSerializer(order).data)


# ---------- Stripe payment: create payment intent ----------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_pay(request, order_id):
    """
    Create Stripe PaymentIntent and return client_secret.
    Frontend should use Stripe.js to confirm payment with client_secret.
    """
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.payment_method != "Stripe":
        return Response({"detail": "Order not set for Stripe"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = int(order.total_amount * 100)  # in paise/cents
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=getattr(settings, "STRIPE_CURRENCY", "inr"),
            metadata={"order_id": str(order.id), "user_id": str(request.user.id)},
        )
        order.stripe_payment_intent = intent["id"]
        order.save(update_fields=["stripe_payment_intent"])
        return Response({"client_secret": intent["client_secret"], "payment_intent": intent["id"]})
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------- Stripe webhook (mark as paid) ----------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)
    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            # without signature verification (dev only)
            event = json.loads(payload.decode("utf-8"))
    except Exception:
        return HttpResponse(status=400)

    # Payment succeeded
    if isinstance(event, dict) and event.get("type") == "payment_intent.succeeded":
        pi = event.get("data", {}).get("object", {})
        metadata = pi.get("metadata", {})
        order_id = metadata.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                order.payment_status = "Paid"
                order.order_status = "Processing"
                order.save(update_fields=["payment_status", "order_status"])
            except Order.DoesNotExist:
                pass

    # If using stripe library construct_event, event is stripe.Event - handle same type key:
    if not isinstance(event, dict) and getattr(event, "type", "") == "payment_intent.succeeded":
        pi = event.data.object
        metadata = getattr(pi, "metadata", {})
        order_id = metadata.get("order_id")
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                order.payment_status = "Paid"
                order.order_status = "Processing"
                order.save(update_fields=["payment_status", "order_status"])
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)


# ---------- Auth: signup & profile ----------
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "username & password required"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "username taken"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(UserSerializer(request.user).data)
