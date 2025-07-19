from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Main site URLs
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('contact/', views.contact, name='contact'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('shipping-info/', views.shipping_info, name='shipping_info'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),
    
    # Payment callback
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    
    # Client Admin URLs
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/products/', views.client_products, name='client_products'),
    path('client/orders/', views.client_orders, name='client_orders'),
    path('client/customers/', views.client_customers, name='client_customers'),
    path('client/reports/', views.client_reports, name='client_reports'),
    path('client/export/', views.client_export_data, name='client_export_data'),
] 