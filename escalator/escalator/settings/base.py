# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_URL = os.getenv('ESCALATOR_BASE_URL', '')
TWILIO_SID = os.getenv('ESCALATOR_TWILIO_SID', '')
TWILIO_TOKEN = os.getenv('ESCALATOR_TWILIO_TOKEN', '')
TWILIO_OUTGOING = os.getenv('ESCALATOR_TWILIO_OUTGOING', '')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('ESCALATOR_GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('ESCALATOR_GOOGLE_OAUTH2_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_LOGIN_REDIRECT_URL = '/dashboard/'
SOCIAL_AUTH_GOOGLE_OAUTH2_NEW_USER_REDIRECT_URL = '/start/'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p7n1^4h#$4&ei!d00cbyl3f1$g)t+26ovid#o7f_7f)f3ih!@d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'social.apps.django_app.default',
    'djrill',
    'waffle',
    'guardian',
    'invite',
    'organization',
    'conference',
    'dashboard',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

ROOT_URLCONF = 'escalator.urls'

WSGI_APPLICATION = 'escalator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
    'social.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
)


ANONYMOUS_USER_ID = 0

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
