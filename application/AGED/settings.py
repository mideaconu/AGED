# 
# settings.py
#
# Author: Mihai Ionut Deaconu
#

import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '_^ob=pwzf(!0e--7zu4q$h4i@-jnsldutkf-@_mkaecmbbc2cg'

DEBUG = True

BOOTSTRAP3 = {
    "css_url": {
        "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
        "integrity": "sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
        "crossorigin": "anonymous",
    },

    "theme_url": None,

    "javascript_url": {
        "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
        "integrity": "sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa",
        "crossorigin": "anonymous",
    },

    "jquery_url": "//code.jquery.com/jquery.min.js",

    "javascript_in_head": False,

    "include_jquery": False,

    "horizontal_label_class": "col-md-3",

    "horizontal_field_class": "col-md-9",

    "set_placeholder": True,

    "required_css_class": "",

    "error_css_class": "has-error",

    "success_css_class": "has-success",

    "formset_renderers":{
        "default": "bootstrap3.renderers.FormsetRenderer",
    },
    "form_renderers": {
        "default": "bootstrap3.renderers.FormRenderer",
    },
    "field_renderers": {
        "default": "bootstrap3.renderers.FieldRenderer",
        "inline": "bootstrap3.renderers.InlineFieldRenderer",
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'import_export',
    'bootstrap3',
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', 
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
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

ROOT_URLCONF = 'AGED.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'AGED.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # tells which database engine to use
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # name of the db
    }
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

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en-US',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIAL_AUTH_FACEBOOK_KEY = '2169514156709372'
SOCIAL_AUTH_FACEBOOK_SECRET = 'af5cf2b67032f7b5fb2942f8c35878cb'

SITE_ID = 1

IMPORT_EXPORT_USE_TRANSACTIONS = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day in seconds
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/' 
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True

PROJECT_DIR = os.path.dirname(__file__)

STATIC_ROOT= os.path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = '0029aged@gmail.com'
EMAIL_HOST_PASSWORD = 'COMP0029IndividualProject'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 

ALLOWED_HOSTS = ['localhost', '127.0.0.1']