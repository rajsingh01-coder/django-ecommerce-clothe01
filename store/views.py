from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm, CartItemForm, SearchForm, ContactForm
from django.conf import settings
from django.utils import timezone


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
    paginator = Paginator(products, 12)
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
                    recipient_list=[order.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                # Send admin notification
                admin_subject = f"New Order Received - {order.order_number}"
                admin_message = f"""
                नया Order आया है!
                
                Order Details:
                Order Number: {order.order_number}
                Customer: {order.first_name} {order.last_name}
                Email: {order.email}
                Phone: {order.phone}
                Total Amount: ₹{order.total_amount}
                
                Shipping Address:
                {order.address}
                {order.city}, {order.state} {order.pincode}
                
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
        # Pre-fill form with user data if available
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)
    
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
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],  # आपका email
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'Failed to send message: {str(e)}')
            
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