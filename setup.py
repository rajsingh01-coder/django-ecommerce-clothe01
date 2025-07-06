#!/usr/bin/env python
"""
Setup script for Django E-commerce Clothing Store
This script helps with initial project setup and configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("\n📝 Creating .env file...")
        env_content = """# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (MongoDB)
DB_NAME=ecommerce_clothes
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=
DB_PASSWORD=

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security Settings
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the .env file with your actual configuration")
    else:
        print("✅ .env file already exists")

def check_python_version():
    """Check if Python version is compatible"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ is required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def run_migrations():
    """Run Django migrations"""
    return run_command("python manage.py makemigrations", "Creating migrations") and \
           run_command("python manage.py migrate", "Running migrations")

def create_superuser():
    """Create a superuser"""
    print("\n👤 Creating superuser...")
    print("Please enter the following information for the admin user:")
    
    # Set environment variables for non-interactive superuser creation
    os.environ['DJANGO_SUPERUSER_USERNAME'] = 'admin'
    os.environ['DJANGO_SUPERUSER_EMAIL'] = 'admin@example.com'
    os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'admin123'
    
    return run_command("python manage.py createsuperuser --noinput", "Creating superuser")

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def main():
    """Main setup function"""
    print("🚀 Django E-commerce Clothing Store Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Setup failed at migrations")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser():
        print("\n❌ Setup failed at superuser creation")
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        print("\n❌ Setup failed at static file collection")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start MongoDB (if using local installation)")
    print("2. Update .env file with your configuration")
    print("3. Run: python manage.py runserver")
    print("4. Visit: http://127.0.0.1:8000")
    print("5. Admin panel: http://127.0.0.1:8000/admin")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n⚠️  Important:")
    print("- Change the default admin password")
    print("- Update SECRET_KEY in .env file for production")
    print("- Configure your MongoDB connection")

if __name__ == "__main__":
    main() 