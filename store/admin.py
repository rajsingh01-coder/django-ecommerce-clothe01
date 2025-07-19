from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import Category, Product, ProductImage, Cart, CartItem, Order, OrderItem, Contact, ClientAdmin
import json
import csv
from datetime import datetime
from django.contrib.auth import get_user_model


# Import/Export Resources
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        import_id_fields = ('id',)
        export_order = ('id', 'name', 'slug', 'description', 'created_at', 'updated_at')


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ('id',)
        export_order = ('id', 'name', 'slug', 'description', 'price', 'sale_price', 'category', 'stock', 'is_featured', 'is_active', 'created_at')


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        import_id_fields = ('id',)
        export_order = ('id', 'order_number', 'user', 'total_amount', 'status', 'payment_status', 'created_at')


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        import_id_fields = ('id',)
        export_order = ('id', 'name', 'email', 'subject', 'message', 'created_at', 'is_read')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'image')
        }),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'brand', 'category', 'price', 'sale_price', 'stock', 'is_featured', 'is_active', 'created_at', 'image_preview']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_editable = ['price', 'sale_price', 'stock', 'is_featured', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


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
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ['order_number', 'user', 'phone_number', 'total_amount', 'status', 'payment_status', 'created_at', 'quick_actions']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'phone_number']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'total_amount']
    list_per_page = 20
    
    actions = ['approve_orders', 'process_orders', 'ship_orders', 'deliver_orders', 'cancel_orders', 'export_to_json', 'export_to_csv']
    
    def quick_actions(self, obj):
        actions = []
        if obj.status == 'pending':
            actions.append(f'<a href="?action=approve&id={obj.id}" class="button">✅ Approve</a>')
        elif obj.status == 'processing':
            actions.append(f'<a href="?action=ship&id={obj.id}" class="button">📦 Ship</a>')
        elif obj.status == 'shipped':
            actions.append(f'<a href="?action=deliver&id={obj.id}" class="button">🎯 Deliver</a>')
        
        actions.append(f'<a href="?action=view&id={obj.id}" class="button">👁️ View</a>')
        return format_html(' '.join(actions))
    quick_actions.short_description = 'Quick Actions'
    
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
    
    def export_to_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        data = []
        for order in queryset:
            order_data = {
                'order_number': order.order_number,
                'user': order.user.username,
                'total_amount': str(order.total_amount),
                'status': order.status,
                'payment_status': order.payment_status,
                'created_at': order.created_at.isoformat(),
                'items': []
            }
            for item in order.items.all():
                order_data['items'].append({
                    'product': item.product.name,
                    'quantity': item.quantity,
                    'price': str(item.price),
                    'size': item.size,
                    'color': item.color
                })
            data.append(order_data)
        
        json.dump(data, response, indent=2)
        return response
    export_to_json.short_description = "📄 Export selected orders to JSON"
    
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order Number', 'User', 'Total Amount', 'Status', 'Payment Status', 'Created At'])
        
        for order in queryset:
            writer.writerow([
                order.order_number,
                order.user.username,
                order.total_amount,
                order.status,
                order.payment_status,
                order.created_at
            ])
        
        return response
    export_to_csv.short_description = "📊 Export selected orders to CSV"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Calculate total_amount from order items (if any)
        total = 0
        for item in obj.items.all():
            total += item.price * item.quantity
        obj.total_amount = total
        # Save again only if there are items
        if obj.items.exists():
            obj.save()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'size', 'color', 'get_total_price']
    list_filter = ['size', 'color']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['get_total_price']


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read', 'mark_as_read']
    list_filter = ['created_at', 'is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_per_page = 20
    actions = ['mark_as_read_action', 'mark_as_unread', 'export_to_json']
    
    def mark_as_read(self, obj):
        if obj.is_read:
            return "✅ Read"
        return format_html('<a href="?action=mark_read&id={}" class="button">📖 Mark as Read</a>', obj.id)
    mark_as_read.short_description = 'Read Status'
    
    def mark_as_read_action(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages have been marked as read.')
    mark_as_read_action.short_description = "📖 Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} messages have been marked as unread.')
    mark_as_unread.short_description = "📝 Mark selected messages as unread"
    
    def export_to_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="contacts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        data = []
        for contact in queryset:
            data.append({
                'name': contact.name,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message,
                'created_at': contact.created_at.isoformat(),
                'is_read': contact.is_read
            })
        
        json.dump(data, response, indent=2)
        return response
    export_to_json.short_description = "📄 Export selected contacts to JSON"


@admin.register(ClientAdmin)
class ClientAdminAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'phone', 'is_active', 'permissions_summary', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['company_name', 'user__username', 'phone']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'phone', 'address')
        }),
        ('Permissions', {
            'fields': ('can_manage_products', 'can_manage_orders', 'can_manage_customers', 'can_view_reports')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def permissions_summary(self, obj):
        permissions = []
        if obj.can_manage_products:
            permissions.append('Products')
        if obj.can_manage_orders:
            permissions.append('Orders')
        if obj.can_manage_customers:
            permissions.append('Customers')
        if obj.can_view_reports:
            permissions.append('Reports')
        return ', '.join(permissions) if permissions else 'None'
    permissions_summary.short_description = 'Permissions'


# Custom Admin Site
class EcommerceAdminSite(admin.AdminSite):
    site_header = "🛍️ E-Commerce Fashion Store - Admin Panel"
    site_title = "E-Commerce Admin"
    index_title = "Welcome to E-Commerce Admin Panel"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('data-export/', self.admin_view(self.data_export_view), name='data-export'),
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def data_export_view(self, request):
        """Data export functionality"""
        if request.method == 'POST':
            export_type = request.POST.get('export_type')
            model_name = request.POST.get('model')
            
            if export_type == 'json':
                return self.export_data_json(request, model_name)
            elif export_type == 'csv':
                return self.export_data_csv(request, model_name)
        
        return admin.views.index(request)
    
    def export_data_json(self, request, model_name):
        """Export data to JSON format"""
        models_map = {
            'products': Product,
            'categories': Category,
            'orders': Order,
            'contacts': Contact,
        }
        
        if model_name in models_map:
            model = models_map[model_name]
            queryset = model.objects.all()
            
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{model_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
            
            data = []
            for obj in queryset:
                data.append(self.serialize_object(obj))
            
            json.dump(data, response, indent=2)
            return response
        
        messages.error(request, 'Invalid model selected')
        return redirect('admin:index')
    
    def export_data_csv(self, request, model_name):
        """Export data to CSV format"""
        models_map = {
            'products': Product,
            'categories': Category,
            'orders': Order,
            'contacts': Contact,
        }
        
        if model_name in models_map:
            model = models_map[model_name]
            queryset = model.objects.all()
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{model_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
            
            writer = csv.writer(response)
            
            # Write headers
            if model == Product:
                writer.writerow(['Name', 'Category', 'Price', 'Sale Price', 'Stock', 'Is Featured', 'Is Active'])
                for obj in queryset:
                    writer.writerow([
                        obj.name,
                        obj.category.name if obj.category else '',
                        obj.price,
                        obj.sale_price or '',
                        obj.stock,
                        obj.is_featured,
                        obj.is_active
                    ])
            elif model == Category:
                writer.writerow(['Name', 'Slug', 'Description', 'Created At'])
                for obj in queryset:
                    writer.writerow([obj.name, obj.slug, obj.description, obj.created_at])
            elif model == Order:
                writer.writerow(['Order Number', 'User', 'Total Amount', 'Status', 'Payment Status', 'Created At'])
                for obj in queryset:
                    writer.writerow([
                        obj.order_number,
                        obj.user.username,
                        obj.total_amount,
                        obj.status,
                        obj.payment_status,
                        obj.created_at
                    ])
            elif model == Contact:
                writer.writerow(['Name', 'Email', 'Subject', 'Message', 'Created At', 'Is Read'])
                for obj in queryset:
                    writer.writerow([
                        obj.name,
                        obj.email,
                        obj.subject,
                        obj.message,
                        obj.created_at,
                        obj.is_read
                    ])
            
            return response
        
        messages.error(request, 'Invalid model selected')
        return redirect('admin:index')
    
    def serialize_object(self, obj):
        """Serialize Django model object to dictionary"""
        data = {}
        for field in obj._meta.fields:
            value = getattr(obj, field.name)
            if hasattr(value, 'isoformat'):  # DateTime fields
                data[field.name] = value.isoformat()
            elif hasattr(value, 'username'):  # User fields
                data[field.name] = value.username
            elif hasattr(value, 'name'):  # ForeignKey fields
                data[field.name] = value.name
            else:
                data[field.name] = str(value)
        return data
    
    def dashboard_view(self, request):
        """Custom dashboard with statistics"""
        from django.db.models import Count, Sum
        from django.utils import timezone
        from datetime import timedelta
        
        # Get statistics
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_users = get_user_model().objects.count()
        total_revenue = Order.objects.filter(payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Recent orders
        recent_orders = Order.objects.order_by('-created_at')[:10]
        
        # Monthly revenue
        thirty_days_ago = timezone.now() - timedelta(days=30)
        monthly_revenue = Order.objects.filter(
            created_at__gte=thirty_days_ago,
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        context = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'recent_orders': recent_orders,
        }
        
        return admin.views.index(request, extra_context=context)


# Create custom admin site instance
admin_site = EcommerceAdminSite(name='ecommerce_admin')

# Register models with custom admin site
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(Cart, CartAdmin)
admin_site.register(CartItem, CartItemAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderItem, OrderItemAdmin)
admin_site.register(Contact, ContactAdmin)
admin_site.register(ClientAdmin, ClientAdminAdmin) 