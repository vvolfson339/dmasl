from .base import *
import json

with open('/etc/dmasl_config.json') as config_file:
    config = json.load(config_file)

DEBUG = True

SECRET_KEY = config['SECRET_KEY']

ALLOWED_HOSTS = ['159.89.146.14', 'dmasl.ca', 'www.dmasl.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config['MySQL_DB_Name'],
        'USER': config['MySQL_DB_User'],
        'PASSWORD': config['MySQL_DB_Pass'],
        'HOST': config['MySQL_DB_Host'],
    }
}
