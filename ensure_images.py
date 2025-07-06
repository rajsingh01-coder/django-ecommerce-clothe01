#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_clothes.settings')
django.setup()

from store.models import Product

def ensure_product_images():
    """Ensure all products have proper image URLs and some are featured"""
    products = Product.objects.all()
    
    # Good quality Unsplash image URLs
    image_urls = [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
    ]
    
    import random
    updated_count = 0
    featured_count = 0
    
    for i, product in enumerate(products):
        # Ensure product has a valid image URL
        if not product.image_url or not product.image_url.startswith('http'):
            product.image_url = random.choice(image_urls)
            updated_count += 1
        
        # Mark some products as featured (about 20%)
        if i < 30 and not product.is_featured:  # First 30 products
            product.is_featured = True
            featured_count += 1
        
        product.save()
    
    print(f"Updated {updated_count} products with image URLs")
    print(f"Marked {featured_count} products as featured")
    print(f"Total products: {products.count()}")

if __name__ == '__main__':
    ensure_product_images() 