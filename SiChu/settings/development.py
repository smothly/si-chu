from .base import *

secrets = secret_base["DEVELOPMENT"]

SECRET_KEY = '#-*rn3rb+%c%h)znyc0rc0p0e@41e7&*%x_-02e1y9swq5=@1c'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email test with Console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
