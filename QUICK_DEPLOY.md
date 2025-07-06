# 🚀 Quick Deployment Guide - Railway

## Step 1: Create GitHub Repository
1. Go to https://github.com/rajsingh01-coder
2. Click "New repository"
3. Name: `django-ecommerce-clothes`
4. Make it **Public**
5. Click "Create repository"

## Step 2: Push to GitHub
Run these commands in your terminal:
```bash
git remote add origin https://github.com/rajsingh01-coder/django-ecommerce-clothes.git
git push -u origin main
```

## Step 3: Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `django-ecommerce-clothes` repository
6. Railway will automatically deploy your app!

## Step 4: Configure Environment Variables
In Railway dashboard, add these environment variables:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
EMAIL_HOST_USER=singhraj23036@gmail.com
EMAIL_HOST_PASSWORD=23037
```

## Step 5: Add Database
1. In Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically connect it to your app

## Step 6: Get Your Live URL
Railway will give you a URL like: `https://your-app-name.railway.app`

## Alternative: Render.com
If Railway doesn't work, try Render:
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your repository
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn ecommerce_clothes.wsgi`

Your website will be live in 5-10 minutes! 🎉 