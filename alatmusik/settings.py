# alatmusik/settings.py

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# KONFIGURASI INTI & KEAMANAN UNTUK PRODUKSI
# ==============================================================================

# Baca SECRET_KEY dari environment variable di Railway.
# Jangan pernah menuliskan secret key asli di sini.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-local-development')

# DEBUG akan False di Railway (jika Anda mengatur env var), dan True di lokal.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Konfigurasi ALLOWED_HOSTS yang dinamis dan aman.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','web-production-0c0f.up.railway.app']
RAILWAY_HOSTNAME = os.environ.get('RAILWAY_STATIC_URL') 
if RAILWAY_HOSTNAME:
    ALLOWED_HOSTS.append(RAILWAY_HOSTNAME.replace("https://", ""))

# ==============================================================================
# APLIKASI & MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Menambahkan Whitenoise
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
    # Aplikasi Anda
    'rest_framework',
    'alatmusik_app',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise Middleware harus berada tepat di bawah SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# PENGATURAN URL & TEMPLATE
# ==============================================================================

ROOT_URLCONF = 'alatmusik.urls'
WSGI_APPLICATION = 'alatmusik.wsgi.application'

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

# ==============================================================================
# DATABASE (Fleksibel untuk Lokal dan Produksi)
# ==============================================================================

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================================================
# FILE STATIS (Dikonfigurasi untuk Whitenoise)
# ==============================================================================

STATIC_URL = '/static/'
# Tempat di mana `collectstatic` akan mengumpulkan semua file statis.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Penyimpanan yang direkomendasikan untuk Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# PENGATURAN KEAMANAN PRODUKSI (Sangat Penting)
# ==============================================================================

# Jika tidak dalam mode DEBUG (yaitu di Railway), aktifkan pengaturan keamanan ini
if not DEBUG:
    # Ini memberitahu Django untuk mempercayai header dari proxy Railway (memperbaiki POST -> GET)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Ini memberitahu Django untuk mempercayai permintaan POST dari domain Railway Anda
    if RAILWAY_HOSTNAME:
        CSRF_TRUSTED_ORIGINS = ['https://' + RAILWAY_HOSTNAME.replace("https://", "")]

# ==============================================================================
# PENGATURAN LAINNYA
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Mengatur kebijakan perizinan default untuk semua view.
    # 'AllowAny' berarti tidak ada otentikasi atau perizinan yang dibutuhkan.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
