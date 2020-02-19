"""
WSGI config for SiChu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
    
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiChu.settings')
# gcp
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',
                      './SiChu/.gcp/cred.json')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SiChu.settings.production')

application = get_wsgi_application()
