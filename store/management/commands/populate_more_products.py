from django.core.management.base import BaseCommand
from store.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Add 200 more products with different images'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please run populate_data first.'))
            return
        
        # More Unsplash image URLs for different clothing items
        image_urls = [
            # T-Shirts
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
            
            # Jeans
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop",
            
            # Dresses
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop",
            
            # Shirts
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop",
            
            # Hoodies
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
            
            # Jackets
            "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
            
            # Sweaters
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop",
            
            # Skirts
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop",
            
            # Shorts
            "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=400&fit=crop",
        ]
        
        # Product names for different categories
        product_names = {
            'T-Shirts': [
                'Classic Cotton T-Shirt', 'Premium V-Neck Tee', 'Graphic Print T-Shirt', 'Striped T-Shirt',
                'Polo T-Shirt', 'Long Sleeve T-Shirt', 'Slim Fit T-Shirt', 'Oversized T-Shirt',
                'Crew Neck T-Shirt', 'Henley T-Shirt', 'Ringer T-Shirt', 'Pocket T-Shirt',
                'Triblend T-Shirt', 'Performance T-Shirt', 'Organic Cotton Tee', 'Retro T-Shirt',
                'Athletic T-Shirt', 'Fashion T-Shirt', 'Basic T-Shirt', 'Designer T-Shirt'
            ],
            'Jeans': [
                'Slim Fit Jeans', 'Straight Leg Jeans', 'Bootcut Jeans', 'Skinny Jeans',
                'Relaxed Fit Jeans', 'High Waist Jeans', 'Low Rise Jeans', 'Distressed Jeans',
                'Dark Wash Jeans', 'Light Wash Jeans', 'Black Jeans', 'Colored Jeans',
                'Mom Jeans', 'Boyfriend Jeans', 'Flare Jeans', 'Wide Leg Jeans',
                'Cropped Jeans', 'Jeggings', 'Vintage Jeans', 'Premium Denim Jeans'
            ],
            'Dresses': [
                'Summer Dress', 'Cocktail Dress', 'Maxi Dress', 'Mini Dress',
                'Wrap Dress', 'Shift Dress', 'Bodycon Dress', 'A-Line Dress',
                'Empire Waist Dress', 'Fit and Flare Dress', 'Sheath Dress', 'Pencil Dress',
                'Floral Dress', 'Solid Color Dress', 'Print Dress', 'Evening Dress',
                'Casual Dress', 'Formal Dress', 'Party Dress', 'Office Dress'
            ],
            'Shirts': [
                'Oxford Shirt', 'Dress Shirt', 'Casual Shirt', 'Polo Shirt',
                'Button Down Shirt', 'Flannel Shirt', 'Denim Shirt', 'Linen Shirt',
                'Chambray Shirt', 'Poplin Shirt', 'Twill Shirt', 'Cotton Shirt',
                'Silk Shirt', 'Satin Shirt', 'Plaid Shirt', 'Striped Shirt',
                'Solid Shirt', 'Print Shirt', 'Long Sleeve Shirt', 'Short Sleeve Shirt'
            ],
            'Hoodies': [
                'Pullover Hoodie', 'Zip Up Hoodie', 'Fleece Hoodie', 'Cotton Hoodie',
                'Athletic Hoodie', 'Fashion Hoodie', 'Oversized Hoodie', 'Slim Fit Hoodie',
                'Graphic Hoodie', 'Solid Hoodie', 'Striped Hoodie', 'Colorblock Hoodie',
                'Winter Hoodie', 'Summer Hoodie', 'Lightweight Hoodie', 'Heavyweight Hoodie',
                'Crop Hoodie', 'Long Hoodie', 'Cropped Hoodie', 'Designer Hoodie'
            ],
            'Jackets': [
                'Denim Jacket', 'Leather Jacket', 'Bomber Jacket', 'Blazer',
                'Cardigan', 'Windbreaker', 'Rain Jacket', 'Winter Jacket',
                'Spring Jacket', 'Summer Jacket', 'Casual Jacket', 'Formal Jacket',
                'Athletic Jacket', 'Fashion Jacket', 'Vintage Jacket', 'Modern Jacket',
                'Lightweight Jacket', 'Heavy Jacket', 'Cropped Jacket', 'Long Jacket'
            ],
            'Sweaters': [
                'Crew Neck Sweater', 'V-Neck Sweater', 'Turtle Neck Sweater', 'Cardigan Sweater',
                'Pullover Sweater', 'Cable Knit Sweater', 'Chunky Sweater', 'Lightweight Sweater',
                'Wool Sweater', 'Cotton Sweater', 'Cashmere Sweater', 'Acrylic Sweater',
                'Striped Sweater', 'Solid Sweater', 'Patterned Sweater', 'Oversized Sweater',
                'Fitted Sweater', 'Cropped Sweater', 'Long Sweater', 'Designer Sweater'
            ],
            'Skirts': [
                'A-Line Skirt', 'Pencil Skirt', 'Pleated Skirt', 'Maxi Skirt',
                'Mini Skirt', 'Midi Skirt', 'Wrap Skirt', 'Tulip Skirt',
                'Circle Skirt', 'Straight Skirt', 'Flared Skirt', 'Tiered Skirt',
                'Denim Skirt', 'Leather Skirt', 'Cotton Skirt', 'Silk Skirt',
                'Casual Skirt', 'Formal Skirt', 'Summer Skirt', 'Winter Skirt'
            ],
            'Shorts': [
                'Denim Shorts', 'Cotton Shorts', 'Athletic Shorts', 'Cargo Shorts',
                'High Waist Shorts', 'Low Rise Shorts', 'Bermuda Shorts', 'Hot Pants',
                'Paper Bag Shorts', 'Pleated Shorts', 'Linen Shorts', 'Chino Shorts',
                'Casual Shorts', 'Dress Shorts', 'Summer Shorts', 'Beach Shorts',
                'Gym Shorts', 'Fashion Shorts', 'Vintage Shorts', 'Designer Shorts'
            ],
            'Shoes': [
                'Sneakers', 'Running Shoes', 'Casual Shoes', 'Dress Shoes',
                'Boots', 'Sandals', 'Flats', 'Heels',
                'Loafers', 'Oxfords', 'Derby Shoes', 'Brogues',
                'Athletic Shoes', 'Fashion Shoes', 'Comfortable Shoes', 'Stylish Shoes',
                'Summer Shoes', 'Winter Shoes', 'Spring Shoes', 'Fall Shoes'
            ],
            'Accessories': [
                'Handbag', 'Backpack', 'Wallet', 'Belt',
                'Scarf', 'Hat', 'Sunglasses', 'Jewelry',
                'Watch', 'Gloves', 'Socks', 'Underwear',
                'Fashion Accessories', 'Stylish Accessories', 'Trendy Accessories', 'Classic Accessories',
                'Summer Accessories', 'Winter Accessories', 'Spring Accessories', 'Fall Accessories'
            ]
        }
        
        # Product descriptions
        descriptions = [
            "Premium quality fabric with excellent comfort and durability.",
            "Stylish design perfect for any casual occasion.",
            "Comfortable fit with modern styling for everyday wear.",
            "High-quality material that feels great against your skin.",
            "Versatile piece that can be dressed up or down.",
            "Trendy design that's perfect for the current season.",
            "Comfortable and stylish for all-day wear.",
            "Premium construction with attention to detail.",
            "Perfect blend of style and comfort for any occasion.",
            "High-quality fabric that maintains its shape and color.",
            "Modern design with excellent fit and comfort.",
            "Versatile piece that works with any outfit.",
            "Comfortable fit with stylish design elements.",
            "Premium quality with excellent durability.",
            "Trendy design perfect for fashion-forward individuals.",
            "Comfortable and stylish for everyday wear.",
            "High-quality material with excellent breathability.",
            "Versatile design that suits multiple occasions.",
            "Premium construction with modern styling.",
            "Comfortable fit with excellent quality fabric."
        ]
        
        # Colors and sizes
        colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Yellow', 'Pink', 'Purple', 'Orange', 'Brown', 'Gray', 'Navy']
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        
        products_created = 0
        
        for category in categories:
            category_name = category.name
            if category_name in product_names:
                names = product_names[category_name]
                
                for i in range(20):  # 20 products per category = 200 total
                    name = f"{names[i % len(names)]} #{i+1}"
                    description = random.choice(descriptions)
                    price = random.randint(500, 5000)  # INR prices
                    sale_price = price * 0.8 if random.random() < 0.3 else None  # 30% chance of sale
                    stock = random.randint(10, 100)
                    is_featured = random.random() < 0.2  # 20% chance of being featured
                    
                    # Select random image
                    image_url = random.choice(image_urls)
                    
                    # Random colors and sizes
                    available_colors = random.sample(colors, random.randint(3, 6))
                    available_sizes = random.sample(sizes, random.randint(4, 6))
                    
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        price=price,
                        sale_price=sale_price,
                        category=category,
                        available_colors=available_colors,
                        available_sizes=available_sizes,
                        stock=stock,
                        is_featured=is_featured,
                        image_url=image_url
                    )
                    
                    products_created += 1
                    
                    if products_created % 50 == 0:
                        self.stdout.write(f"Created {products_created} products...")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {products_created} additional products!')
        ) 