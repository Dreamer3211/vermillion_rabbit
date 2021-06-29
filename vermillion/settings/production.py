from .base import *

DEBUG = False
SECRET_KEY = 'mv4$m#ik+t_s)9@0*4&#%39gm$43_jbzo&6yepzq%*w(f#3-(a'
ALLOWED_HOSTS = ['localhost', 'vermillionrabbit.com','*']
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND":
        "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache",
    }
}

DATABASES = {
    "default":{
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'vermillionrabbit',
        "USER": 'vermillionrabbit',
        "PASSWORD": 'xfHjB^F29s*zhqFT6cNx2',
        "HOST": 'localhost',
        "PORT": "",
    }
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://326c36f68f9d4cec9ccc270df613268c@o886548.ingest.sentry.io/5838012",
    integrations=[DjangoIntegration()],
    
    traces_sample_rate=1.0,
    
    send_default_pii=True 
)


try:
    from .local import *
except ImportError:
    pass
