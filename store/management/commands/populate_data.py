from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate database with categories and products'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Men\'s T-Shirts',
                'description': 'Comfortable and stylish t-shirts for men',
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop'
            },
            {
                'name': 'Women\'s Dresses',
                'description': 'Elegant dresses for every occasion',
                'image': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop'
            },
            {
                'name': 'Jeans',
                'description': 'Classic and trendy jeans for all',
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop'
            },
            {
                'name': 'Sneakers',
                'description': 'Comfortable and stylish sneakers',
                'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop'
            },
            {
                'name': 'Hoodies',
                'description': 'Warm and cozy hoodies',
                'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop'
            },
            {
                'name': 'Shirts',
                'description': 'Formal and casual shirts',
                'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop'
            },
            {
                'name': 'Skirts',
                'description': 'Elegant skirts for women',
                'image': 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop'
            },
            {
                'name': 'Jackets',
                'description': 'Stylish jackets for all seasons',
                'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop'
            },
            {
                'name': 'Sweaters',
                'description': 'Warm and comfortable sweaters',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'
            },
            {
                'name': 'Accessories',
                'description': 'Fashion accessories and jewelry',
                'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop'
            }
        ]

        # Create categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'image': cat_data['image']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products for each category
        products_data = {
            'Men\'s T-Shirts': [
                {'name': 'Classic White T-Shirt', 'price': 25.00, 'description': 'Premium cotton white t-shirt', 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop'},
                {'name': 'Black Graphic T-Shirt', 'price': 30.00, 'description': 'Stylish black t-shirt with graphic design', 'image': 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=400&fit=crop'},
                {'name': 'Striped T-Shirt', 'price': 28.00, 'description': 'Comfortable striped t-shirt', 'image': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop'}
            ],
            'Women\'s Dresses': [
                {'name': 'Summer Floral Dress', 'price': 65.00, 'description': 'Beautiful floral summer dress', 'image': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop'},
                {'name': 'Evening Gown', 'price': 120.00, 'description': 'Elegant evening gown', 'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop'},
                {'name': 'Casual Maxi Dress', 'price': 45.00, 'description': 'Comfortable casual maxi dress', 'image': 'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?w=400&h=400&fit=crop'}
            ],
            'Jeans': [
                {'name': 'Classic Blue Jeans', 'price': 55.00, 'description': 'Classic blue denim jeans', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop'},
                {'name': 'Black Skinny Jeans', 'price': 60.00, 'description': 'Stylish black skinny jeans', 'image': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop'},
                {'name': 'Distressed Jeans', 'price': 70.00, 'description': 'Trendy distressed jeans', 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop'}
            ],
            'Sneakers': [
                {'name': 'White Canvas Sneakers', 'price': 45.00, 'description': 'Classic white canvas sneakers', 'image': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop'},
                {'name': 'Running Shoes', 'price': 85.00, 'description': 'Comfortable running shoes', 'image': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=400&fit=crop'},
                {'name': 'Casual Sneakers', 'price': 65.00, 'description': 'Stylish casual sneakers', 'image': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop'}
            ],
            'Hoodies': [
                {'name': 'Gray Pullover Hoodie', 'price': 40.00, 'description': 'Comfortable gray hoodie', 'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop'},
                {'name': 'Black Zip Hoodie', 'price': 45.00, 'description': 'Stylish black zip hoodie', 'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop'},
                {'name': 'Colorful Hoodie', 'price': 50.00, 'description': 'Vibrant colorful hoodie', 'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop'}
            ],
            'Shirts': [
                {'name': 'White Formal Shirt', 'price': 35.00, 'description': 'Classic white formal shirt', 'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop'},
                {'name': 'Plaid Casual Shirt', 'price': 40.00, 'description': 'Stylish plaid casual shirt', 'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop'},
                {'name': 'Denim Shirt', 'price': 45.00, 'description': 'Classic denim shirt', 'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop'}
            ],
            'Skirts': [
                {'name': 'A-Line Skirt', 'price': 35.00, 'description': 'Elegant A-line skirt', 'image': 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop'},
                {'name': 'Pleated Skirt', 'price': 40.00, 'description': 'Stylish pleated skirt', 'image': 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop'},
                {'name': 'Maxi Skirt', 'price': 50.00, 'description': 'Long maxi skirt', 'image': 'https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop'}
            ],
            'Jackets': [
                {'name': 'Leather Jacket', 'price': 120.00, 'description': 'Classic leather jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop'},
                {'name': 'Denim Jacket', 'price': 65.00, 'description': 'Stylish denim jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop'},
                {'name': 'Bomber Jacket', 'price': 85.00, 'description': 'Trendy bomber jacket', 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop'}
            ],
            'Sweaters': [
                {'name': 'Cable Knit Sweater', 'price': 55.00, 'description': 'Warm cable knit sweater', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'},
                {'name': 'Turtleneck Sweater', 'price': 45.00, 'description': 'Stylish turtleneck sweater', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'},
                {'name': 'Cardigan Sweater', 'price': 50.00, 'description': 'Comfortable cardigan sweater', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'}
            ],
            'Accessories': [
                {'name': 'Leather Belt', 'price': 25.00, 'description': 'Classic leather belt', 'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop'},
                {'name': 'Silver Necklace', 'price': 35.00, 'description': 'Elegant silver necklace', 'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop'},
                {'name': 'Sunglasses', 'price': 30.00, 'description': 'Stylish sunglasses', 'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop'}
            ]
        }

        # Create products
        for category_name, products in products_data.items():
            category = Category.objects.get(name=category_name)
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    category=category,
                    defaults={
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'image_url': product_data['image'],
                        'stock': 50
                    }
                )
                if created:
                    self.stdout.write(f'Created product: {product.name} in {category.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with categories and products')) 