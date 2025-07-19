from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import timedelta
from .models import *
from .forms import *
import json
import csv
from django.views.decorators.csrf import csrf_exempt

# Initialize Razorpay client conditionally
try:
    import razorpay
    razorpay_client = None
except ImportError:
    razorpay_client = None

def home(request):
    """Homepage with featured products and categories"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()[:6]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'home.html', context)


def product_list(request):
    """Product listing with search and filters"""
    products = Product.objects.filter(is_active=True)
    search_form = SearchForm(request.GET)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'search_form': search_form,
        'categories': Category.objects.all(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart_item_form = CartItemForm(product=product)
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'cart_item_form': cart_item_form,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def category_detail(request, slug):
    """Category detail page"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
    }
    return render(request, 'store/category_detail.html', context)


def get_or_create_cart(request):
    """Helper function to get or create cart for user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    
    return cart


def cart_detail(request):
    """Shopping cart detail page"""
    cart = get_or_create_cart(request)
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        if item_id and action:
            try:
                item = CartItem.objects.get(id=item_id, cart=cart)
                if action == 'update':
                    quantity = int(request.POST.get('quantity', 1))
                    if quantity > 0:
                        item.quantity = quantity
                        item.save()
                        messages.success(request, 'Cart updated successfully!')
                    else:
                        item.delete()
                        messages.success(request, 'Item removed from cart!')
                elif action == 'remove':
                    item.delete()
                    messages.success(request, 'Item removed from cart!')
            except CartItem.DoesNotExist:
                messages.error(request, 'Item not found in cart!')
        
        return redirect('store:cart_detail')
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart via AJAX"""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        cart = get_or_create_cart(request)
        
        form = CartItemForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data.get('size', '')
            color = form.cleaned_data.get('color', '')
            
            # Check if item already exists in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                size=size,
                color=color,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart!',
                'cart_total': cart.get_total_items()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid form data',
                'errors': form.errors
            })
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        })


@login_required
def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:product_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.get_current_price(),
                    size=cart_item.size,
                    color=cart_item.color
                )
            
            # Create Razorpay order (only if razorpay is available)
            if razorpay_client:
                try:
                    razorpay_order = razorpay_client.order.create({
                        'amount': int(order.total_amount * 100),  # Convert to paise
                        'currency': 'INR',
                        'receipt': order.order_number,
                        'notes': {
                            'order_id': order.order_number,
                            'user_id': str(request.user.id)
                        }
                    })
                    
                    order.razorpay_order_id = razorpay_order['id']
                    order.save()
                except Exception as e:
                    messages.warning(request, f'Payment gateway not configured: {str(e)}')
            
            # Send order confirmation email
            try:
                # Render email template
                html_message = render_to_string('emails/order_confirmation.html', {
                    'order': order,
                })
                plain_message = strip_tags(html_message)
                
                # Send email to customer
                send_mail(
                    subject=f'Order Confirmation - {order.order_number}',
                    message=plain_message,
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL
                    recipient_list=[order.user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                # Send admin notification
                admin_subject = f"New Order Received - {order.order_number}"
                admin_message = f"""
                नया Order आया है!
                
                Order Details:
                Order Number: {order.order_number}
                Customer: {order.user.get_full_name() or order.user.username}
                Email: {order.user.email}
                Phone: {order.phone_number}
                Total Amount: ₹{order.total_amount}
                
                Shipping Address:
                {order.shipping_address}
                
                Order Items:
                """
                
                for item in order.items.all():
                    admin_message += f"- {item.product.name} (Qty: {item.quantity}, Price: ₹{item.price})\n"
                
                admin_message += f"""
                
                Order Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
                Status: {order.status}
                
                Admin Panel: http://127.0.0.1:8000/admin/store/order/{order.id}/change/
                """
                
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],  # आपका email
                    fail_silently=False,
                )
                
                messages.success(request, f'Order confirmation email sent to {order.email}!')
                
            except Exception as e:
                messages.warning(request, f'Order placed successfully, but email could not be sent: {str(e)}')
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('store:order_detail', order_number=order.order_number)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_detail(request, order_number):
    """Order detail page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)


def about(request):
    return render(request, 'store/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save contact form to database
            contact = form.save()
            
            # Send email to admin
            subject = f"New Contact Form Submission from {form.cleaned_data['name']}"
            message = f"""
            नया Contact Form Submission आया है!
            
            Customer Details:
            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Subject: {form.cleaned_data['subject']}
            Message: {form.cleaned_data['message']}
            
            Date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            Contact ID: {contact.id}
            
            Admin Panel: http://127.0.0.1:8000/admin/store/contact/{contact.id}/change/
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],  # आपका email
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            except Exception as e:
                messages.warning(request, f'Message saved but email could not be sent: {str(e)}')
            
            return redirect('store:contact')
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {'form': form})

def service(request):
    return render(request, 'store/service.html')

def test_email(request):
    """Test email functionality"""
    try:
        subject = 'Test Email from E-commerce Site'
        message = f"""
        This is a test email from your e-commerce website.
        
        Email Configuration:
        - Host: {settings.EMAIL_HOST}
        - Port: {settings.EMAIL_PORT}
        - User: {settings.EMAIL_HOST_USER}
        - From: {settings.DEFAULT_FROM_EMAIL}
        
        If you receive this email, your email configuration is working correctly!
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Test email sent successfully to {settings.ADMIN_EMAIL}'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Email error: {str(e)}'
        })

def shipping_info(request):
    return render(request, 'store/shipping_info.html')

def returns(request):
    return render(request, 'store/returns.html')

def faq(request):
    return render(request, 'store/faq.html')

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            # Get payment data
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            # Verify signature
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update order
            order = Order.objects.get(razorpay_order_id=order_id)
            order.payment_status = 'completed'
            order.payment_method = 'Razorpay'
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.save()
            
            messages.success(request, 'Payment successful! Your order has been placed.')
            return redirect('store:order_detail', order_number=order.order_number)
            
        except Exception as e:
            messages.error(request, f'Payment verification failed: {str(e)}')
            return redirect('store:order_history')
    
    return redirect('store:order_history') 

# Client Admin Views
def is_client_admin(user):
    """Check if user is a client admin"""
    return hasattr(user, 'clientadmin') and user.clientadmin.is_active

@login_required
@user_passes_test(is_client_admin)
def client_dashboard(request):
    """Client admin dashboard"""
    client_admin = request.user.clientadmin
    
    # Get statistics based on permissions
    context = {
        'client_admin': client_admin,
        'total_products': 0,
        'total_orders': 0,
        'total_customers': 0,
        'total_revenue': 0,
        'recent_orders': [],
        'monthly_revenue': 0,
    }
    
    if client_admin.can_manage_products:
        context['total_products'] = Product.objects.count()
    
    if client_admin.can_manage_orders:
        context['total_orders'] = Order.objects.count()
        context['total_revenue'] = Order.objects.filter(
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Monthly revenue
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['monthly_revenue'] = Order.objects.filter(
            created_at__gte=thirty_days_ago,
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Recent orders
        context['recent_orders'] = Order.objects.order_by('-created_at')[:10]
    
    if client_admin.can_manage_customers:
        context['total_customers'] = User.objects.filter(is_staff=False).count()
    
    return render(request, 'store/client_dashboard.html', context)

@login_required
@user_passes_test(is_client_admin)
def client_products(request):
    """Client admin products management"""
    if not request.user.clientadmin.can_manage_products:
        messages.error(request, "You don't have permission to manage products.")
        return redirect('store:client_dashboard')
    
    products = Product.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    
    return render(request, 'store/client_products.html', context)

@login_required
@user_passes_test(is_client_admin)
def client_orders(request):
    """Client admin orders management"""
    if not request.user.clientadmin.can_manage_orders:
        messages.error(request, "You don't have permission to manage orders.")
        return redirect('store:client_dashboard')
    
    orders = Order.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    payment_status_filter = request.GET.get('payment_status', '')
    if payment_status_filter:
        orders = orders.filter(payment_status=payment_status_filter)
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'payment_status_filter': payment_status_filter,
        'status_choices': Order.STATUS_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
    }
    
    return render(request, 'store/client_orders.html', context)

@login_required
@user_passes_test(is_client_admin)
def client_customers(request):
    """Client admin customers management"""
    if not request.user.clientadmin.can_manage_customers:
        messages.error(request, "You don't have permission to manage customers.")
        return redirect('store:client_dashboard')
    
    customers = User.objects.filter(is_staff=False, is_superuser=False)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Get customer statistics
    for customer in customers:
        customer.total_orders = Order.objects.filter(user=customer).count()
        customer.total_spent = Order.objects.filter(
            user=customer, 
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'store/client_customers.html', context)

@login_required
@user_passes_test(is_client_admin)
def client_reports(request):
    """Client admin reports"""
    if not request.user.clientadmin.can_view_reports:
        messages.error(request, "You don't have permission to view reports.")
        return redirect('store:client_dashboard')
    
    # Sales report
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Daily sales for last 30 days
    daily_sales = []
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        sales = Order.objects.filter(
            created_at__date=date,
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        daily_sales.append({
            'date': date,
            'sales': sales
        })
    
    # Top products
    top_products = Product.objects.annotate(
        total_sold=Count('orderitem')
    ).order_by('-total_sold')[:10]
    
    # Top categories
    top_categories = Category.objects.annotate(
        total_products=Count('products'),
        total_sales=Sum('products__orderitem__price')
    ).order_by('-total_sales')[:10]
    
    context = {
        'daily_sales': daily_sales,
        'top_products': top_products,
        'top_categories': top_categories,
        'total_revenue': Order.objects.filter(
            payment_status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_orders': Order.objects.count(),
        'total_customers': User.objects.filter(is_staff=False).count(),
    }
    
    return render(request, 'store/client_reports.html', context)

@login_required
@user_passes_test(is_client_admin)
def client_export_data(request):
    """Export data for client admin"""
    export_type = request.GET.get('type', 'json')
    model_name = request.GET.get('model', '')
    
    if not model_name:
        messages.error(request, "Please specify a model to export.")
        return redirect('store:client_dashboard')
    
    # Check permissions
    client_admin = request.user.clientadmin
    if model_name == 'products' and not client_admin.can_manage_products:
        messages.error(request, "You don't have permission to export products.")
        return redirect('store:client_dashboard')
    elif model_name == 'orders' and not client_admin.can_manage_orders:
        messages.error(request, "You don't have permission to export orders.")
        return redirect('store:client_dashboard')
    elif model_name == 'customers' and not client_admin.can_manage_customers:
        messages.error(request, "You don't have permission to export customers.")
        return redirect('store:client_dashboard')
    
    # Export data
    if export_type == 'json':
        return export_data_json(request, model_name)
    elif export_type == 'csv':
        return export_data_csv(request, model_name)
    else:
        messages.error(request, "Invalid export type.")
        return redirect('store:client_dashboard')

def export_data_json(request, model_name):
    """Export data to JSON format"""
    models_map = {
        'products': Product,
        'orders': Order,
        'customers': User,
    }
    
    if model_name in models_map:
        model = models_map[model_name]
        queryset = model.objects.all()
        
        # Filter customers to exclude staff
        if model == User:
            queryset = queryset.filter(is_staff=False, is_superuser=False)
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        data = []
        for obj in queryset:
            data.append(serialize_object(obj))
        
        json.dump(data, response, indent=2)
        return response
    
    messages.error(request, 'Invalid model selected')
    return redirect('store:client_dashboard')

def export_data_csv(request, model_name):
    """Export data to CSV format"""
    models_map = {
        'products': Product,
        'orders': Order,
        'customers': User,
    }
    
    if model_name in models_map:
        model = models_map[model_name]
        queryset = model.objects.all()
        
        # Filter customers to exclude staff
        if model == User:
            queryset = queryset.filter(is_staff=False, is_superuser=False)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
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
        elif model == User:
            writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'Date Joined'])
            for obj in queryset:
                writer.writerow([
                    obj.username,
                    obj.email,
                    obj.first_name,
                    obj.last_name,
                    obj.date_joined
                ])
        
        return response
    
    messages.error(request, 'Invalid model selected')
    return redirect('store:client_dashboard')

def serialize_object(obj):
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

# Utility function to delete all products and categories (for admin use only)
def delete_all_products_and_categories():
    from store.models import Product, Category
    Product.objects.all().delete()
    Category.objects.all().delete() 