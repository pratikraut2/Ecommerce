# shop/admin.py - FIXED VERSION WITH PROPER IMAGE WIDGET

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, Widget
from django.core.files import File
from django.core.files.storage import default_storage
import os
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# ---------------- CUSTOM IMAGE WIDGET (FIXED) ----------------
class ImageWidget(Widget):
    """Custom widget to handle image imports from file paths"""
    
    def clean(self, value, row=None, **kwargs):
        """Convert file path to Django File object"""
        if not value:
            return None
            
        # Remove any quotes or whitespace
        value = str(value).strip().strip('"').strip("'")
        
        if not value or value.lower() == 'nan':
            return None
            
        # Handle both absolute paths and relative paths
        if value.startswith('products/'):
            # This is the expected format: products/filename.jpg
            file_path = os.path.join('media', value)  # media/products/filename.jpg
        elif value.startswith('media/products/'):
            # Full media path: media/products/filename.jpg
            file_path = value
        else:
            # Assume it's just the filename, add the full path
            file_path = os.path.join('media', 'products', os.path.basename(value))
        
        # Check if file exists
        if os.path.exists(file_path):
            try:
                # Return just the relative path that Django expects
                return value if value.startswith('products/') else f"products/{os.path.basename(value)}"
            except Exception as e:
                print(f"Error processing image {value}: {e}")
                return None
        else:
            print(f"Image file not found: {file_path}")
            return None
    
    def render(self, value, obj=None):
        """Render the value for export"""
        if not value:
            return ""
        
        # If it's a Django ImageField, get the path
        if hasattr(value, 'url'):
            return value.name
        
        # If it's already a string path, return it
        return str(value)


# ---------------- RESOURCES ----------------
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ("id", "name", "description")
        import_id_fields = ("name",)


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category__name',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    
    image = fields.Field(
        column_name='image',
        attribute='image',
        widget=ImageWidget()
    )
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name", 
            "brand",
            "category",
            "description",
            "price",
            "stock", 
            "image",
            "rating",
            "is_active",
        )
        import_id_fields = ("name",)
        
    def before_import_row(self, row, **kwargs):
        """Process each row before import"""
        # Clean up image path
        if 'image' in row:
            image_path = str(row['image']).strip()
            if image_path and image_path.lower() not in ['nan', 'none', '']:
                # Ensure the path is in the correct format
                if not image_path.startswith('products/'):
                    if '/' in image_path:
                        image_path = 'products/' + os.path.basename(image_path)
                    else:
                        image_path = 'products/' + image_path
                row['image'] = image_path
            else:
                row['image'] = ''
        
        return super().before_import_row(row, **kwargs)


# ---------------- ADMINS ----------------
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product) 
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ("name", "brand", "category", "price", "stock", "is_active", "has_image", "created_at")
    list_filter = ("category", "brand", "is_active", "created_at")
    search_fields = ("name", "brand", "description")
    list_editable = ("price", "stock", "is_active")
    ordering = ("-created_at",)
    
    def has_image(self, obj):
        """Show if product has an image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


# ---------------- REST OF YOUR ADMIN CLASSES ----------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total_price")
    search_fields = ("user__username",)
    inlines = [CartItemInline]
    ordering = ("-created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ("total_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "ordered_at", "order_status", "payment_method", "payment_status", "total_amount")
    list_filter = ("order_status", "payment_method", "payment_status", "ordered_at")
    search_fields = ("user__username", "shipping_address")
    inlines = [OrderItemInline]
    readonly_fields = ("ordered_at", "stripe_payment_intent")
    ordering = ("-ordered_at",)


admin.site.register(CartItem)
admin.site.register(OrderItem)