from .base import *
import json

with open('/etc/dmasl_config.json') as config_file:
    config = json.load(config_file)

DEBUG = True

SECRET_KEY = config['SECRET_KEY']

ALLOWED_HOSTS = config['Allowed_Hosts']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'config['MySQL_DB_Name']',
        'USER': 'config['MySQL_DB_User']',
        'PASSWORD': 'config['MySQL_DB_Password']',
        'HOST': 'config['MySQL_DB_Host']',
    }
}
