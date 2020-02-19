from .base import *

secrets = secret_base["PRODUCTION"]

SECRET_KEY = get_conf('SECRET_KEY', secrets)

DEBUG = True

# 배포 후 변경
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.compute.amazonaws.com',
    'sichu.mooo.com',
    '*.sichu.mooo.com',
    'sichu.mooo.com/*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'conf', 'mysql.cnf'),
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" # strict mode 설정 추가
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
