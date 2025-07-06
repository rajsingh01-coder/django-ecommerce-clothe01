# Fashion Store - Django E-commerce Website

A complete Django e-commerce clothing website with MongoDB integration, featuring a modern responsive design and full shopping cart functionality.

## Features

- **Product Catalog**: Browse products by category with search and filtering
- **Shopping Cart**: Add/remove items, update quantities, size/color selection
- **User Authentication**: Registration, login, logout, and profile management
- **Checkout System**: Complete order processing with shipping information
- **Admin Panel**: Full product and order management interface
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **MongoDB Integration**: Using djongo for NoSQL database support
- **Image Upload**: Product and category image management
- **Search & Filters**: Advanced product search and filtering capabilities

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MongoDB with djongo
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in authentication system
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Image Processing**: Pillow
- **Development**: Python 3.8+

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ecommerce_clothes
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=ecommerce_clothes
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=
DB_PASSWORD=
```

### Step 5: Database Setup

1. **Local MongoDB**: Start MongoDB service
2. **MongoDB Atlas**: Use your connection string in settings

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the website.

## Project Structure

```
ecommerce_clothes/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── ecommerce_clothes/       # Main project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── store/                   # Main e-commerce app
│   ├── __init__.py
│   ├── admin.py             # Admin interface
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL patterns
│   └── forms.py             # Form definitions
├── accounts/                # User authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Homepage
│   ├── store/               # Store templates
│   └── accounts/            # Account templates
├── static/                  # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── media/                   # User uploaded files
    ├── products/
    ├── categories/
    └── profile_pics/
```

## Database Models

### Store App Models

- **Category**: Product categories with name, description, and image
- **Product**: Products with name, description, price, images, sizes, colors, stock
- **ProductImage**: Multiple images per product with primary image support
- **Cart**: Shopping cart for users and anonymous sessions
- **CartItem**: Individual items in cart with quantity, size, color
- **Order**: Customer orders with shipping information
- **OrderItem**: Individual items in orders

### Accounts App Models

- **UserProfile**: Extended user profile with address and contact information

## Key Features Implementation

### Product Management

- Product creation with multiple images
- Category organization
- Size and color variants
- Stock management
- Sale pricing support

### Shopping Cart

- Session-based cart for anonymous users
- User-specific cart for authenticated users
- Quantity updates
- Size and color selection
- Cart persistence

### User Authentication

- Custom registration form
- User profile management
- Address information storage
- Profile picture upload

### Admin Interface

- Product management with inline images
- Category management
- Order tracking and management
- User management
- Cart monitoring

## API Endpoints

### Store URLs

- `/` - Homepage
- `/products/` - Product listing with filters
- `/product/<slug>/` - Product detail page
- `/category/<slug>/` - Category products
- `/cart/` - Shopping cart
- `/add-to-cart/<id>/` - Add product to cart (AJAX)
- `/checkout/` - Checkout process
- `/order/<number>/` - Order detail
- `/orders/` - Order history

### Account URLs

- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/profile/` - User profile

## Customization

### Adding New Features

1. **New Product Fields**: Modify `store/models.py`
2. **Custom Templates**: Add templates in `templates/` directory
3. **Additional Apps**: Create new Django apps as needed
4. **Styling**: Modify `static/css/style.css`

### Configuration Options

- **Database**: Change MongoDB connection in `settings.py`
- **Email**: Configure email settings for notifications
- **Payment**: Integrate payment gateways (Stripe, PayPal, etc.)
- **Shipping**: Add shipping calculation logic
- **Tax**: Implement tax calculation based on location

## Deployment

### Production Settings

1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Set up SSL certificate
6. Configure web server (Nginx, Apache)

### Environment Variables

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=production_db_name
DB_HOST=your-mongodb-host
DB_PORT=27017
DB_USERNAME=your-username
DB_PASSWORD=your-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact: support@fashionstore.com

## Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Font Awesome for icons
- MongoDB for database
- All contributors and users

---

**Note**: This is a demo e-commerce website. For production use, implement proper security measures, payment processing, and additional features as needed. 