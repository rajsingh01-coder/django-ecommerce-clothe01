from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the database with 6 categories and 8 products per category, using Unsplash images.'

    def handle(self, *args, **options):
        category_data = [
            {'name': 'Men', 'keyword': 'men fashion'},
            {'name': 'Women', 'keyword': 'women fashion'},
            {'name': 'Kids', 'keyword': 'kids fashion'},
            {'name': 'Accessories', 'keyword': 'fashion accessories'},
            {'name': 'Shoes', 'keyword': 'shoes'},
            {'name': 'Sale', 'keyword': 'clothes sale'},
        ]
        brands = ['Nike', 'Adidas', 'Puma', 'Zara', 'H&M', 'Levis', 'Gucci', 'Uniqlo', 'Reebok', 'Under Armour']
        created_categories = []
        for idx, cat in enumerate(category_data):
            unsplash_url = f'https://source.unsplash.com/600x400/?{cat["keyword"].replace(" ",",")},{idx}'
            category, created = Category.objects.get_or_create(
                name=cat['name'],
                defaults={
                    'description': f'{cat["name"]} category description.',
                    'image': unsplash_url,
                }
            )
            created_categories.append((category, cat['keyword']))
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat["name"]}'))
            else:
                self.stdout.write(f'Category already exists: {cat["name"]}')

        for category, keyword in created_categories:
            for i in range(1, 9):
                brand = brands[(i-1) % len(brands)]
                product_name = f'{category.name} {brand} Item {i}'
                product_keyword = f'{keyword},{brand},clothing,product,{i}'
                unsplash_url = f'https://source.unsplash.com/600x800/?{product_keyword.replace(" ",",")}'
                description = f"{product_name} by {brand}. This is a high-quality, stylish item perfect for the {category.name.lower()} category. Features premium materials and modern design."
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        'description': description,
                        'price': 49.99 + i,
                        'stock': 10 * i,
                        'is_featured': True,
                        'is_active': True,
                        'image_url': unsplash_url,
                        'available_sizes': ['S', 'M', 'L'],
                        'available_colors': ['Red', 'Blue', 'Green'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product_name}'))
                else:
                    self.stdout.write(f'Product already exists: {product_name}')

        self.stdout.write(self.style.SUCCESS('Database population complete.')) 