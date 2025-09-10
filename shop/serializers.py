from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product, Cart, CartItem, Order, OrderItem

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source="category", queryset=Category.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ("id", "name", "brand", "description", "price", "stock", "image", "rating", "is_active", "category", "category_id")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, source="product", queryset=Product.objects.filter(is_active=True))

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "created_at", "items", "total_price")
        read_only_fields = ("user", "created_at", "items", "total_price")

    def get_total_price(self, obj):
        return obj.total_price()


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price", "total_price")
        read_only_fields = ("total_price",)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user", "ordered_at", "shipping_address", "order_status", "payment_method", "payment_status", "total_amount", "order_items", "stripe_payment_intent")
        read_only_fields = ("id", "user", "ordered_at", "order_status", "payment_status", "total_amount", "order_items", "stripe_payment_intent")
