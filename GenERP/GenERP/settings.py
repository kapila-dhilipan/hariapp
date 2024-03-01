from pathlib import Path
import os
from dotenv import load_dotenv
import psycopg2
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format=" %(asctime)s - %(name)s -%(levelname)s -%(message)s ")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Loading environment variables from .env file
envars = BASE_DIR / ".env"
if os.path.exists(envars):
    load_dotenv(envars)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s^5im*((diw(&$(7f3=tv(-=$del1l4100(np3+gebbd$j2o=k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TRACKER_ON = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'admin_interface',
    'colorfield', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    # Local apps
    "hrms",
    'authentication',
    'django_user_agents',
    # 'django_filters',
    # 'crispy_forms',
    # 'django_countries',
    # 'phonenumber_field',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',
    # 'zxcvbn_password',
    # 'ckeditor',
    # 'ckeditor_uploader',
    # 'bootstrap5',
    # 'django_celery_results',
    # 'import_export',
]


SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Third party middleware📌
    # 'defender.middleware.FailedLoginMiddleware',
    # 'django_otp.middleware.OTPMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'GenERP.urls'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
# Thousand separator symbol
THOUSAND_SEPARATOR = ','

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'GenERP.wsgi.application'
 
# Database
# Database settings for the POSTGRESQL connection -- clever-cloud service
# if os.getenv("POSTGRESQL_ADDON_DB"):
#     try:
#         DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.postgresql',
#                 'NAME': os.getenv("POSTGRESQL_ADDON_DB"),
#                 'USER': os.getenv("POSTGRESQL_ADDON_USER"),
#                 'PASSWORD': os.getenv("POSTGRESQL_ADDON_PASSWORD"),
#                 'HOST': os.getenv("POSTGRESQL_ADDON_HOST"),  # or the address of your PostgreSQL server
#                 'PORT': '5432', 
#             },
#             'local': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': BASE_DIR / 'SQLITE3-hari.db'
#             }
#         }
#     except Exception as e:
#         # logging.error("Error connecting to PostgreSQL: %s", str(e))
#         print('There seems to be error in the network/moving onto a local storage')

     
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'SQLITE3.db'
    }
}



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'C:\\Users\\Trainee\\vscode\\django\\GenERP\\caches',
    }
}



##################
# AUTHENTICATION #
##################

# AUTH_USER_MODEL = 'authentication.User'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = '/accounts/login/'

X_FRAME_OPTIONS='SAMEORIGIN'
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

# # Celery Configurations
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP MODULE SETTINGS
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'mail.sightspectrum.in'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv("E-MAIL")
EMAIL_HOST_PASSWORD = os.getenv("SMTP_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("E-MAIL")


#######           For Tracking the visitors using their IP ADDRESS         #######
GEOIP_PATH = BASE_DIR / "GeoIP_data"
