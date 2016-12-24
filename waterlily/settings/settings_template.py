from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<secret key>'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db name>',
        'USER': '<db user>',
        'PASSWORD': '<db password>',
        'HOST': '<db host>',
        'PORT': '',
    }
}


SERVER_EMAIL = "<server email>"
EMAIL_HOST = "<email host>"
EMAIL_PORT = "<email port>"
EMAIL_HOST_USER = "<email_id>"
EMAIL_HOST_PASSWORD = "<password>"
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = "<subject prefix>"

ORDER_IMAGE_LOCATION = "/srv/media/images/order/"
ORDER_IMAGE_BASE_URL = "http://cdn1.baramasi.com/media/images/order/"

ADMINS = [('Waterlily Admin', 'neerajshukla1911@gmail.com')]
