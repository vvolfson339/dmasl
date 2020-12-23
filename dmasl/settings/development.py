from .base import *

SECRET_KEY = 'u7z$z&=bltmwm9ywd^4pz1^$+lu@lj-0_n3r14@6or-0ee34jl'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
