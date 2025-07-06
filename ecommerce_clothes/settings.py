"""
Django settings for ecommerce_clothes project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'accounts',
]

# Try to import crispy forms, add to INSTALLED_APPS if available
try:
    import crispy_forms
    INSTALLED_APPS.append('crispy_forms')
    try:
        import crispy_bootstrap5
        INSTALLED_APPS.append('crispy_bootstrap5')
    except ImportError:
        pass
except ImportError:
    pass

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_clothes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_clothes.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Using SQLite for easy setup - change to MongoDB later
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MongoDB Configuration (uncomment when MongoDB is available)
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': os.environ.get('DB_NAME', 'ecommerce_clothes'),
#         'ENFORCE_SCHEMA': True,
#         'CLIENT': {
#             'host': os.environ.get('DB_HOST', 'localhost'),
#             'port': int(os.environ.get('DB_PORT', 27017)),
#             'username': os.environ.get('DB_USERNAME', ''),
#             'password': os.environ.get('DB_PASSWORD', ''),
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms (optional)
try:
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"
except NameError:
    pass

# Authentication settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Email Configuration for Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'singhraj23036@gmail.com'
EMAIL_HOST_PASSWORD = '23037'  # Your Gmail password
DEFAULT_FROM_EMAIL = 'singhraj23036@gmail.com'

# Admin email for order notifications
ADMIN_EMAIL = 'singhraj23036@gmail.com'  # Admin email for order notifications

# ⚠️ IMPORTANT: You need to generate Gmail App Password for email to work! ⚠️
# 
# Steps to get Gmail App Password:
# 1. Go to your Gmail account settings: https://myaccount.google.com/
# 2. Go to Security → 2-Step Verification (enable it if not already enabled)
# 3. Go to Security → App Passwords
# 4. Select "Mail" and "Other (Custom name)"
# 5. Enter a name like "Django E-commerce"
# 6. Click "Generate"
# 7. Copy the 16-character password (e.g., "abcd efgh ijkl mnop")
# 8. Replace '23037' above with your actual App Password
# 
# Example: EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'
# 
# Without this, contact form and order emails will fail! 