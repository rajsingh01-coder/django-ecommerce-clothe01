from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import ClientAdmin


class Command(BaseCommand):
    help = 'Create a client admin user with specified permissions'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the client admin')
        parser.add_argument('email', type=str, help='Email for the client admin')
        parser.add_argument('password', type=str, help='Password for the client admin')
        parser.add_argument('company_name', type=str, help='Company name for the client admin')
        
        parser.add_argument('--phone', type=str, default='', help='Phone number')
        parser.add_argument('--address', type=str, default='', help='Address')
        
        parser.add_argument('--no-products', action='store_true', help='Disable product management')
        parser.add_argument('--no-orders', action='store_true', help='Disable order management')
        parser.add_argument('--no-customers', action='store_true', help='Disable customer management')
        parser.add_argument('--no-reports', action='store_true', help='Disable reports access')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        company_name = options['company_name']
        phone = options['phone']
        address = options['address']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User "{username}" already exists!')
            )
            return
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'Email "{email}" is already registered!')
            )
            return
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create client admin profile
            client_admin = ClientAdmin.objects.create(
                user=user,
                company_name=company_name,
                phone=phone,
                address=address,
                can_manage_products=not options['no_products'],
                can_manage_orders=not options['no_orders'],
                can_manage_customers=not options['no_customers'],
                can_view_reports=not options['no_reports']
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Client admin "{username}" created successfully!')
            )
            
            # Display permissions
            permissions = []
            if client_admin.can_manage_products:
                permissions.append('Products')
            if client_admin.can_manage_orders:
                permissions.append('Orders')
            if client_admin.can_manage_customers:
                permissions.append('Customers')
            if client_admin.can_view_reports:
                permissions.append('Reports')
            
            self.stdout.write(f'📋 Company: {company_name}')
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔐 Permissions: {", ".join(permissions) if permissions else "None"}')
            self.stdout.write(f'🌐 Client Admin URL: http://127.0.0.1:8000/client/dashboard/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating client admin: {e}')
            ) 