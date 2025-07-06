#!/usr/bin/env python
"""
Railway Deployment Script
Automatically deploys Django ecommerce project to Railway
"""
import os
import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_railway_cli():
    """Check if Railway CLI is installed"""
    print("🔍 Checking Railway CLI installation...")
    result = subprocess.run("railway --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Railway CLI not found. Installing...")
        install_result = subprocess.run("npm install -g @railway/cli", shell=True, capture_output=True, text=True)
        if install_result.returncode != 0:
            print("❌ Failed to install Railway CLI")
            print("Please install manually: npm install -g @railway/cli")
            return False
    print("✅ Railway CLI is ready")
    return True

def deploy_to_railway():
    """Main deployment function"""
    print("🚀 Starting Railway Deployment...")
    
    # Step 1: Check Railway CLI
    if not check_railway_cli():
        return False
    
    # Step 2: Login to Railway
    print("\n🔐 Logging into Railway...")
    login_result = subprocess.run("railway login", shell=True, input="\n", text=True)
    if login_result.returncode != 0:
        print("❌ Failed to login to Railway")
        return False
    
    # Step 3: Initialize Railway project
    print("\n📁 Initializing Railway project...")
    init_result = subprocess.run("railway init", shell=True, capture_output=True, text=True)
    if init_result.returncode != 0:
        print("❌ Failed to initialize Railway project")
        return False
    
    # Step 4: Add PostgreSQL database
    print("\n🗄️ Adding PostgreSQL database...")
    db_result = subprocess.run("railway add", shell=True, capture_output=True, text=True)
    if db_result.returncode != 0:
        print("❌ Failed to add database")
        return False
    
    # Step 5: Set environment variables
    print("\n⚙️ Setting environment variables...")
    env_vars = [
        "DEBUG=False",
        "SECRET_KEY=django-insecure-production-key-12345",
        "ALLOWED_HOSTS=.railway.app",
        "EMAIL_HOST=smtp.gmail.com",
        "EMAIL_PORT=587",
        "EMAIL_USE_TLS=True",
        "EMAIL_HOST_USER=your-email@gmail.com",
        "EMAIL_HOST_PASSWORD=your-app-password",
        "RAILWAY_ENVIRONMENT=production"
    ]
    
    for var in env_vars:
        set_result = subprocess.run(f"railway variables set {var}", shell=True, capture_output=True, text=True)
        if set_result.returncode != 0:
            print(f"⚠️ Warning: Failed to set {var}")
    
    # Step 6: Deploy to Railway
    print("\n🚀 Deploying to Railway...")
    deploy_result = subprocess.run("railway up", shell=True, capture_output=True, text=True)
    if deploy_result.returncode != 0:
        print("❌ Deployment failed")
        print(f"Error: {deploy_result.stderr}")
        return False
    
    # Step 7: Get the deployment URL
    print("\n🌐 Getting deployment URL...")
    url_result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
    if url_result.returncode == 0:
        domain = url_result.stdout.strip()
        print(f"✅ Your app is deployed at: https://{domain}")
    else:
        print("⚠️ Could not get domain automatically")
    
    # Step 8: Run migrations
    print("\n🗃️ Running database migrations...")
    migrate_result = subprocess.run("railway run python manage.py migrate", shell=True, capture_output=True, text=True)
    if migrate_result.returncode != 0:
        print("❌ Migration failed")
        print(f"Error: {migrate_result.stderr}")
    else:
        print("✅ Migrations completed")
    
    # Step 9: Collect static files
    print("\n📦 Collecting static files...")
    static_result = subprocess.run("railway run python manage.py collectstatic --noinput", shell=True, capture_output=True, text=True)
    if static_result.returncode != 0:
        print("❌ Static files collection failed")
        print(f"Error: {static_result.stderr}")
    else:
        print("✅ Static files collected")
    
    # Step 10: Populate data
    print("\n📊 Populating database with sample data...")
    data_result = subprocess.run("railway run python manage.py populate_data", shell=True, capture_output=True, text=True)
    if data_result.returncode != 0:
        print("❌ Data population failed")
        print(f"Error: {data_result.stderr}")
    else:
        print("✅ Sample data populated")
    
    more_data_result = subprocess.run("railway run python manage.py populate_more_products", shell=True, capture_output=True, text=True)
    if more_data_result.returncode != 0:
        print("❌ Additional data population failed")
        print(f"Error: {more_data_result.stderr}")
    else:
        print("✅ Additional products populated")
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Visit your Railway dashboard to get the exact URL")
    print("2. Test your website")
    print("3. Create a superuser: railway run python manage.py createsuperuser")
    print("4. Check if images are loading properly")
    
    return True

if __name__ == "__main__":
    print("🚀 Django Ecommerce Railway Deployment Script")
    print("=" * 50)
    
    success = deploy_to_railway()
    
    if success:
        print("\n✅ Deployment completed successfully!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1) 