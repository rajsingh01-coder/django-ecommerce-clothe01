#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_clothes.settings')
django.setup()

from store.models import Product

def test_image_urls():
    """Test product image URLs"""
    products = Product.objects.all()[:5]  # Get first 5 products
    
    for product in products:
        print(f"Product: {product.name}")
        print(f"Image URL: {product.image_url}")
        print(f"URL starts with http: {product.image_url.startswith('http') if product.image_url else False}")
        print("-" * 50)

if __name__ == '__main__':
    test_image_urls() 