"""
==========================================
MASTER SYSTEM CONFIGURATION (settings.py)
==========================================
This is the Control Room of the XISHAAN Pharmacy project.
It contains all the core configurations for the database, installed applications, 
security middleware, and session management.

For production deployment, ensure DEBUG is set to False and the SECRET_KEY 
is securely stored in environment variables.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ==========================================
# 0. ENVIRONMENT VAULT INITIALIZATION
# ==========================================
# Load the hidden environment variables from the .env file.
# This ensures sensitive data is never hardcoded into the source code.
load_dotenv()

# ==========================================
# 1. CORE DIRECTORY & SECURITY SETTINGS
# ==========================================
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cryptographic key used for session signing and password hashing.
SECRET_KEY = os.getenv('SECRET_KEY')

# Security switch: MUST be False in production to prevent data leaks.
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Dynamic host resolution: Reads from deployment env or falls back to local addresses
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,*").split(",")
    if host.strip()
]

# ==========================================
# 2. APPLICATION REGISTRY
# ==========================================
INSTALLED_APPS = [
    # Core Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Project Apps
    'store',   # The Main Pharmacy POS & Inventory Application
]


# ==========================================
# 3. MIDDLEWARE & ROUTING ENGINE
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The Main Highway for URL routing
ROOT_URLCONF = 'pharmacy_project.urls'
WSGI_APPLICATION = 'pharmacy_project.wsgi.application'


# ==========================================
# 4. FRONTEND TEMPLATE ENGINE
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['store/templates'],   # Custom HTML folder registered here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================
# 5. DATABASE CONFIGURATION
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# 6. PASSWORD SECURITY & VALIDATORS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- ENTERPRISE POS SECURITY SETTINGS ---
# 1. Instantly log out the user if they close the browser window
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 2. Automatically log out anyone who is inactive for 30 minutes (1800 seconds)
SESSION_COOKIE_AGE = 1800


# ==========================================
# 7. REGIONAL & STATIC FILES
# ==========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# URL used to access static files (CSS, JS, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # -->new line