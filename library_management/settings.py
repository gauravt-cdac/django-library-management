import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = ["*"]  # Custom: Allow all hosts during development

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',                     # Added: Provides API framework support
    'rest_framework_simplejwt',           # Added: Enables JWT authentication
    'corsheaders',                        # Added: Allows handling of CORS
    'books',                              # Custom app for managing books and admin user model
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Added: Handles cross-origin requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'library_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Using MySQL as the database
        'NAME': 'library_db',
        'USER': 'root',
        'PASSWORD': 'gaurav',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom REST Framework configuration:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWT for API authentication
    ),
    'DEFAULT_RENDERER_CLASSES': (  
        'rest_framework.renderers.JSONRenderer',  # Force JSON responses for API consistency
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow public access (modify in production)
    ],
}

# Custom CORS & CSRF settings:
CORS_ALLOW_ALL_ORIGINS = True       # Allow requests from any origin (development only)
CORS_ALLOW_CREDENTIALS = True       # Allow cookies with cross-origin requests
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:8000"]  # Trusted origins for CSRF protection

AUTH_USER_MODEL = 'books.AdminUser'  # Custom: Use a custom user model from the books app

STATIC_URL = 'static/'
