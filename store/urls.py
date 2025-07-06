from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    
    # Test email
    path('test-email/', views.test_email, name='test_email'),
    
    # Cart functionality
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
    
    # New shipping info, returns, and FAQ pages
    path('shipping-info/', views.shipping_info, name='shipping_info'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),
] 