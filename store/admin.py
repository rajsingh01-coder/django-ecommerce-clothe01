from django.contrib import admin
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem, Contact


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'sale_price', 'stock', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_editable = ['price', 'sale_price', 'stock', 'is_featured', 'is_active']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['get_total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'get_total_price', 'get_total_items', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    inlines = [CartItemInline]
    readonly_fields = ['get_total_price', 'get_total_items']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'size', 'color', 'get_total_price', 'created_at']
    list_filter = ['created_at', 'size', 'color']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['get_total_price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'first_name', 'last_name', 'total_amount', 'status', 'created_at', 'get_status_actions']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'total_amount']
    list_per_page = 20
    
    actions = ['approve_orders', 'process_orders', 'ship_orders', 'deliver_orders', 'cancel_orders']
    
    def get_status_actions(self, obj):
        if obj.status == 'pending':
            return f'<a href="?action=approve&id={obj.id}" class="button">Approve</a>'
        elif obj.status == 'processing':
            return f'<a href="?action=ship&id={obj.id}" class="button">Ship</a>'
        elif obj.status == 'shipped':
            return f'<a href="?action=deliver&id={obj.id}" class="button">Deliver</a>'
        else:
            return obj.get_status_display()
    get_status_actions.short_description = 'Quick Actions'
    get_status_actions.allow_tags = True
    
    def approve_orders(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders have been approved and are now processing.')
    approve_orders.short_description = "✅ Approve selected orders (Processing)"
    
    def process_orders(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders are now being processed.')
    process_orders.short_description = "🔄 Mark orders as Processing"
    
    def ship_orders(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders have been shipped.')
    ship_orders.short_description = "📦 Mark orders as Shipped"
    
    def deliver_orders(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders have been delivered.')
    deliver_orders.short_description = "✅ Mark orders as Delivered"
    
    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} orders have been cancelled.')
    cancel_orders.short_description = "❌ Cancel selected orders"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'size', 'color', 'get_total_price']
    list_filter = ['size', 'color']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['get_total_price']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_per_page = 20
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} contact messages marked as read.')
    mark_as_read.short_description = "✅ Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} contact messages marked as unread.')
    mark_as_unread.short_description = "📧 Mark selected messages as unread" 