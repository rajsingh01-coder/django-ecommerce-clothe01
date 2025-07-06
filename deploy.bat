@echo off
echo 🚀 Django Ecommerce Railway Deployment
echo ======================================

echo.
echo Step 1: Checking Railway CLI...
railway --version
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Please install it first.
    pause
    exit /b 1
)

echo.
echo Step 2: Logging into Railway...
railway login
if %errorlevel% neq 0 (
    echo ❌ Login failed
    pause
    exit /b 1
)

echo.
echo Step 3: Initializing Railway project...
railway init
if %errorlevel% neq 0 (
    echo ❌ Project initialization failed
    pause
    exit /b 1
)

echo.
echo Step 4: Adding PostgreSQL database...
railway add
if %errorlevel% neq 0 (
    echo ❌ Database addition failed
    pause
    exit /b 1
)

echo.
echo Step 5: Setting environment variables...
railway variables set DEBUG=False
railway variables set SECRET_KEY=django-insecure-production-key-12345
railway variables set ALLOWED_HOSTS=.railway.app
railway variables set EMAIL_HOST=smtp.gmail.com
railway variables set EMAIL_PORT=587
railway variables set EMAIL_USE_TLS=True
railway variables set EMAIL_HOST_USER=your-email@gmail.com
railway variables set EMAIL_HOST_PASSWORD=your-app-password
railway variables set RAILWAY_ENVIRONMENT=production

echo.
echo Step 6: Deploying to Railway...
railway up
if %errorlevel% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

echo.
echo Step 7: Getting domain...
railway domain

echo.
echo Step 8: Running migrations...
railway run python manage.py migrate

echo.
echo Step 9: Collecting static files...
railway run python manage.py collectstatic --noinput

echo.
echo Step 10: Populating sample data...
railway run python manage.py populate_data
railway run python manage.py populate_more_products

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📋 Next steps:
echo 1. Visit your Railway dashboard to get the exact URL
echo 2. Test your website
echo 3. Create a superuser: railway run python manage.py createsuperuser
echo 4. Check if images are loading properly
echo.
pause 