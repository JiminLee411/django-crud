"""
Django settings for crud project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+u5pnv=kg)^av)1b5#y!%e2pft0cf=2_u3yq+qzdls-7e1p(=q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # allauth 사용을 위해 추가
    'allauth',
    'django.contrib.sites',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao', # 원하는 소셜 사이트

    'accounts',
    'bootstrap4',
    'pages',
    'articles',
    'django.contrib.admin', # admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages', # messages framework
    'django.contrib.staticfiles', # static file
    'django_extensions',
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

ROOT_URLCONF = 'crud.urls'

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

WSGI_APPLICATION = 'crud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# static file들을 모두 모아서 해당 URL로 표현된다. (물리 폴더를 뜻하는 것이 아니다.)
# /static/bootstrap
# /static/articles/style.css
STATIC_URL = '/static/' 
# static file 물리 위치 지정
# 기본적으로 app에 있는 static 폴더들을 모두 관리하며, 아래에 임의의 폴더들을 추가할 수 있다.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crud', 'assets')
]

# MEDIA_ROOT : 실제 미디어 파일이 저장되는 경로
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL : 업로드된 image의 url 주소!
MEDIA_URL = '/media/'

# AUTH
LOGIN_URL = '/accounts/login/' # default! @login_required에서 사용.
AUTH_USER_MODEL = 'accounts.User' # default : auth.User

# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 1 # 'django.contrib.sites' -> 이 앱을 추가하면 무조건 SITE_ID 부여해줘야함
LOGIN_REDIRECT_URL = '/articles/'