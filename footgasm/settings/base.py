"""
Django settings for footgasm project.
Generated by 'django-admin startproject' using Django 3.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x*^@d2q82ow5%191c-j$_in)o)zhltsub!hrvbh^#7(2ut=s_z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


PAYPAL_CLIENT_ID  = "AeP6fpeffBNZW2XN44DKBlDEs2kqdxb0pVDVhCyQ9HuV0JUABqtgFbE6-u6adq8uVTGpufDSQtRy9KgG"
PAYPAL_SECRET_ID  =  "EI-REd7SnivmymP4DikLhxypaP3XYydJTp0VVpGtAn_axVij0P7rYXmYwDZX52CoX028WFyPTAyczgW2"

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'pages.apps.PagesConfig', 
    'staff.apps.StaffConfig',
    'paypal.apps.PaypalConfig', 
    'competitions.apps.CompetitionsConfig',
    'orders.apps.OrdersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]
SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'footgasm.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'footgasm.wsgi.application'

ACCOUNT_ADAPTER = 'footgasm.account_adapter.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'footgasm.account_adapter.SocialAccountAdapter'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION  = "none"
ACCOUNT_SESSION_REMEMBER = True




AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "footgasm/static")
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CELERY_BROKER_URL = 'redis://:1n2S6RjgLoVqTy3FAK61Oo8b4DPAsCUf@redis-17864.c72.eu-west-1-2.ec2.cloud.redislabs.com:17864'
CELERY_RESULT_BACKEND = 'redis://:1n2S6RjgLoVqTy3FAK61Oo8b4DPAsCUf@redis-17864.c72.eu-west-1-2.ec2.cloud.redislabs.com:17864'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', 'smtp.mailgun.org')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '587')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', 'postmaster@sandboxb57bff4e81a147caade9cfe0333f8228.mailgun.org')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', 'd942dd545ab6b6c4e26c9e132216518b-e687bab4-b74cd5d6')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'