#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_clothes.settings')
django.setup()

from store.models import Product, Category

def fix_slug_duplicates():
    """Fix slug duplicates by clearing and recreating products"""
    print("🗑️ Clearing existing products...")
    Product.objects.all().delete()
    print("✅ All products deleted")
    
    print("\n📊 Recreating products with unique slugs...")
    
    # Run the populate commands
    import subprocess
    
    print("Running populate_data...")
    result1 = subprocess.run(["python", "manage.py", "populate_data"], capture_output=True, text=True)
    if result1.returncode == 0:
        print("✅ populate_data completed")
    else:
        print(f"❌ populate_data failed: {result1.stderr}")
    
    print("Running populate_more_products...")
    result2 = subprocess.run(["python", "manage.py", "populate_more_products"], capture_output=True, text=True)
    if result2.returncode == 0:
        print("✅ populate_more_products completed")
    else:
        print(f"❌ populate_more_products failed: {result2.stderr}")
    
    # Count products
    total_products = Product.objects.count()
    print(f"\n📈 Total products created: {total_products}")
    
    # Check for duplicates
    slugs = list(Product.objects.values_list('slug', flat=True))
    unique_slugs = set(slugs)
    
    if len(slugs) == len(unique_slugs):
        print("✅ No duplicate slugs found")
    else:
        print(f"❌ Found {len(slugs) - len(unique_slugs)} duplicate slugs")
    
    return True

if __name__ == '__main__':
    fix_slug_duplicates() 