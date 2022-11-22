"""
For local testing fill out the ommited values and save as local_settings.py

"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cpi_local',
        'USER': 'postgres',
        'PASSWORD': '', # password saved at the time of postgres installation
        'PORT': 5432,
        'HOST':'localhost'
        
    }
}

DEBUG = True
SECURE_SSL_REDIRECT = False
GOOGLE_MAPS_API_KEY = "" # give your own Google API Key

# AWS Storage Credentials
AWS_ACCESS_KEY_ID= ''
AWS_SECRET_ACCESS_KEY=''
AWS_STORAGE_BUCKET_NAME=''

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # For use with gmail
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = '@gmail.com' # Email here
EMAIL_HOST_PASSWORD = '' # Email Password



CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://127.0.0.1:8080'
)

CORS_ORIGIN_ALLOW_ALL = True
