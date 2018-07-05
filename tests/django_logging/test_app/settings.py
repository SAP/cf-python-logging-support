""" Example django test app settings """
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

ROOT_URLCONF = 'tests.django_logging.test_app.urls'

MIDDLEWARE = [
    'sap.cf_logging.django_logging.LoggingMiddleware',
]
