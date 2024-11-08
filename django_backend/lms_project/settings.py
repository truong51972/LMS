"""
Django settings for lms_project project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import logging
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%9tkr6=2x0koih$(9^sggb-z)ub@g$37t*57u7eymim46k+9)w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # or 'bootstrap5'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'role',
    'user',
    'main',
    # 'question_bank', #remove
    'module_group',
    # 'module',
    'training_program',
    'subject',
    'training_program_subjects',
    'category',
    'question',
    'user_module',
    'tools',
    'course',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'lms_project.wsgi.application'

if os.environ.get('USERNAME') == 'tranq':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'LMS_database',
    #         'USER': 'truong51972',
    #         'PASSWORD': '51972',
    #         'HOST': 'localhost',
    #         'PORT': '3306',
    #         'OPTIONS': {
    #             'charset': 'utf8mb4',
    #         },
    #     }
    # }
    AI_API_SERVER = {
        'HOST' : 'localhost',
        'PORT' : '8080',
        'IS_DDNS' : False
    }

elif os.environ.get('USERNAME') == 'truong51972':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'truong51972$LMS_database',
            'USER': 'truong51972',
            'PASSWORD': '@g$37t*57u7eymim46k+9)w',
            'HOST': 'truong51972.mysql.pythonanywhere-services.com',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
    AI_API_SERVER = {
        'HOST' : 'truong51972.ddns.net',
        'PORT' : '8000',
        'IS_DDNS' : True
    }
else:
    database_pwd = os.getenv("MYSQL_ROOT_PASSWORD")
    database_name = os.getenv("MYSQL_DATABASE")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': database_name,
    #         'USER': 'root',
    #         'PASSWORD': database_pwd,
    #         'HOST': 'mysql_database',
    #         'PORT': '3306',
    #         'OPTIONS': {
    #             'charset': 'utf8mb4',
    #         },
    #     }
    # }

    AI_API_SERVER = {
        'HOST' : os.environ.get('AI_API_SERVER_HOST'),
        'PORT' : os.environ.get('AI_API_SERVER_PORT'),
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_TZ = False

USE_I18N = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

# AUTHENTICATION_BACKENDS = [
#     'user.authentication_backends.StaffOnlyBackend',
#     'django.contrib.auth.backends.ModelBackend',  # Đảm bảo backend mặc định vẫn được sử dụng
# ]

LOGIN_URL = '/login/'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# forge to HTTPS protocol for secure
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 năm
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# config for https server
CSRF_TRUSTED_ORIGINS = ['https://truong51972.ddns.net', 'https://lms.truong51972.id.vn']

logging.basicConfig(
    level=logging.INFO, format='%(levelname)-4s - "%(name)s": %(message)s'
)