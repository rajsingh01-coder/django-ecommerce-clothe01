#!/usr/bin/env python
"""
Deployment Test Script for Django E-commerce Website
Run this script to test your deployment configuration locally
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.conf import settings

def test_production_settings():
    """Test production settings"""
    print("🔧 Testing Production Settings...")
    
    # Set environment variables for testing
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_clothes.settings_production')
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-deployment-testing')
    os.environ.setdefault('DEBUG', 'False')
    
    try:
        django.setup()
        print("✅ Production settings loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading production settings: {e}")
        return False

def test_database():
    """Test database connection and migrations"""
    print("\n🗄️ Testing Database...")
    
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        
        # Test migrations
        execute_from_command_line(['manage.py', 'migrate', '--check'])
        print("✅ Database migrations are up to date")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_static_files():
    """Test static files collection"""
    print("\n📁 Testing Static Files...")
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--dry-run'])
        print("✅ Static files collection test successful")
        return True
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def test_email():
    """Test email configuration"""
    print("\n📧 Testing Email Configuration...")
    
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        # Test email settings
        if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
            print(f"✅ Email host configured: {settings.EMAIL_HOST}")
            print(f"✅ Email port configured: {settings.EMAIL_PORT}")
            print(f"✅ Email user configured: {settings.EMAIL_HOST_USER}")
            return True
        else:
            print("❌ Email settings not configured")
            return False
    except Exception as e:
        print(f"❌ Email configuration error: {e}")
        return False

def test_security():
    """Test security settings"""
    print("\n🔒 Testing Security Settings...")
    
    try:
        from django.conf import settings
        
        security_checks = [
            ('DEBUG', settings.DEBUG == False, "Debug should be False in production"),
            ('SECRET_KEY', bool(settings.SECRET_KEY), "Secret key should be set"),
            ('ALLOWED_HOSTS', len(settings.ALLOWED_HOSTS) > 0, "Allowed hosts should be configured"),
        ]
        
        all_passed = True
        for setting, condition, message in security_checks:
            if condition:
                print(f"✅ {setting}: {message}")
            else:
                print(f"❌ {setting}: {message}")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"❌ Security test error: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 Django E-commerce Deployment Test")
    print("=" * 50)
    
    tests = [
        test_production_settings,
        test_database,
        test_static_files,
        test_email,
        test_security,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for deployment.")
        print("\n📋 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Follow the DEPLOYMENT_GUIDE.md")
        print("3. Deploy to Railway, Render, or your preferred platform")
    else:
        print("⚠️ Some tests failed. Please fix the issues before deploying.")
        print("\n🔧 Common fixes:")
        print("- Check your database configuration")
        print("- Verify email settings")
        print("- Ensure all required packages are installed")
        print("- Review the DEPLOYMENT_GUIDE.md for troubleshooting")

if __name__ == '__main__':
    main() 