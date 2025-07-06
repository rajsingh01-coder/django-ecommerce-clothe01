#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_clothes.settings')
django.setup()

from store.models import Product

def fix_image_urls():
    """Fix product image URLs to use direct external URLs"""
    products = Product.objects.all()
    fixed_count = 0
    
    for product in products:
        if product.image_url:
            # Check if the URL is already a direct external URL
            if product.image_url.startswith('http'):
                # URL is already correct, no need to change
                continue
            else:
                # This shouldn't happen with our current data, but just in case
                print(f"Product {product.name} has invalid image URL: {product.image_url}")
                continue
        else:
            # Product has no image URL, assign a default one
            default_images = [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop",
                "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
            ]
            import random
            product.image_url = random.choice(default_images)
            product.save()
            fixed_count += 1
            print(f"Added default image to product: {product.name}")
    
    print(f"Fixed {fixed_count} products with missing image URLs")
    print(f"Total products checked: {products.count()}")

if __name__ == '__main__':
    fix_image_urls() 