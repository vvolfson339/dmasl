from .base import *
import json

with open('/etc/dmasl_config.json') as config_file:
    config = json.load(config_file)

DEBUG = True

SECRET_KEY = config['SECRET_KEY']

#ALLOWED_HOSTS = ['159.89.146.14', 'dmasl.org', 'www.dmasl.org' 'dmasl.ca', 'www.dmasl.ca']
ALLOWED_HOSTS = ['159.89.146.14', 'dmasl.ca', 'www.dmasl.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmasl',
        'USER': 'root',
        'PASSWORD': 'nstu12345678',
        'HOST': 'localhost',
    }
}
