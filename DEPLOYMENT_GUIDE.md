# 🚀 Django E-commerce Website Deployment Guide

## 📋 Prerequisites
- GitHub account
- Python 3.11+ installed locally
- Git installed locally

## 🎯 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)
**Free Tier**: $5 credit monthly

#### Steps:
1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   EMAIL_HOST_USER=singhraj23036@gmail.com
   EMAIL_HOST_PASSWORD=23037
   ```

4. **Add PostgreSQL Database**
   - Go to your project
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set DB environment variables

5. **Deploy**
   - Railway will automatically deploy your app
   - Get your live URL from the dashboard

---

### Option 2: Render (Good Alternative)
**Free Tier**: 750 hours/month

#### Steps:
1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure Build Settings**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn ecommerce_clothes.wsgi
   ```

4. **Add Environment Variables**
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   EMAIL_HOST_USER=singhraj23036@gmail.com
   EMAIL_HOST_PASSWORD=23037
   ```

5. **Add PostgreSQL Database**
   - Create a new PostgreSQL service
   - Link it to your web service

---

### Option 3: PythonAnywhere (Learning Friendly)
**Free Tier**: Limited but good for learning

#### Steps:
1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Sign up for free account

2. **Upload Your Code**
   - Use Git or upload files directly
   - Install requirements: `pip install -r requirements.txt`

3. **Configure WSGI File**
   - Edit the WSGI file to point to your Django app
   - Set up static files

4. **Configure Database**
   - Use SQLite (included) or MySQL (free tier)

---

## 🔧 Local Testing Before Deployment

### 1. Test Production Settings
```bash
python manage.py runserver --settings=ecommerce_clothes.settings_production
```

### 2. Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Test Database Migration
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

---

## 🌐 Domain Configuration

### Custom Domain (Optional)
1. **Railway**: Go to Settings → Domains → Add custom domain
2. **Render**: Go to Settings → Custom Domains → Add domain
3. **Update ALLOWED_HOSTS** in `settings_production.py`

---

## 📧 Email Configuration

### Gmail Setup (Current Configuration)
- **Email**: singhraj23036@gmail.com
- **Password**: 23037
- **SMTP**: smtp.gmail.com:587

### For Production (Recommended)
1. **Enable 2-Step Verification** on Gmail
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → App Passwords
   - Generate password for "Mail"
3. **Update Environment Variables**:
   ```
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   ```

---

## 🔒 Security Checklist

### Before Going Live:
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY`
- [ ] Proper `ALLOWED_HOSTS`
- [ ] HTTPS enabled (if available)
- [ ] Database backups configured
- [ ] Email working
- [ ] Admin user created

---

## 🚨 Troubleshooting

### Common Issues:

1. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database Connection Error**
   - Check environment variables
   - Verify database credentials

3. **Email Not Working**
   - Check Gmail App Password
   - Verify SMTP settings

4. **500 Internal Server Error**
   - Check logs in hosting platform
   - Verify `DEBUG = False` in production

---

## 📞 Support

### Railway Support
- Documentation: [docs.railway.app](https://docs.railway.app)
- Discord: [railway.app/discord](https://railway.app/discord)

### Render Support
- Documentation: [render.com/docs](https://render.com/docs)
- Community: [community.render.com](https://community.render.com)

---

## 🎉 Success!

Once deployed, your e-commerce website will be live at:
- **Railway**: `https://your-app-name.railway.app`
- **Render**: `https://your-app-name.onrender.com`

### Admin Access:
- URL: `your-domain.com/admin/`
- Username: `alpha`
- Password: `alpha23036`

---

## 💡 Pro Tips

1. **Use Environment Variables** for sensitive data
2. **Set up automatic deployments** from GitHub
3. **Monitor your app** using hosting platform tools
4. **Backup your database** regularly
5. **Test thoroughly** before going live

---

**Need Help?** Check the hosting platform's documentation or ask in their community forums! 