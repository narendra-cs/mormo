
import os, sys

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

try:
    config          = __import__('config')
    mongoengine     = __import__('mongoengine')
except ImportError as e:
    print(e.__class__.__name__ + ": " + str(e))
else:
    _cfg  = config.confLoader(os.path.join(BASE_DIR,'mormo_ui.conf'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q+%^(wlv-b2wt76&()y0+9($*9t9y!*asuy-oq_ty2anae5sy='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'mormo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+'/templates'],
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

WSGI_APPLICATION = 'mormo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# mysql Database connection

if 'MYSQL' in _cfg.keys():
    cnf  = _cfg['MYSQL']
    DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql','NAME': cnf['DBNAME'],'USER': cnf['USER'],'PASSWORD': cnf['PASSWD'],'HOST': cnf['HOST'],'PORT': cnf['PORT']}}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': os.path.join(BASE_DIR, 'db.sqlite3')}}

# MongoDB connection

if 'MONGODB' in _cfg.keys():
    cnf  = _cfg['MONGODB']
    MONGODB_DATABASE_URI  = 'mongodb://{user}:{pwd}@{host}:{port}/{db}'.format(user=quote(cnf['USER']),pwd=quote(cnf['PASSWD']),host=cnf['HOST'],port=cnf['PORT'],db=cnf['DBNAME'])

mongoengine.connect(cnf['DBNAME'],host=MONGODB_DATABASE_URI)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,"static_cdn/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# log-in info
LOGIN_URL='/accounts/login'
LOGIN_REDIRECT_URL = '/logs'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR,"media/")
MEDIA_URL = '/media/'
