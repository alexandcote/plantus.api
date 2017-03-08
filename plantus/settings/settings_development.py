
def configure(settings):
    # SECURITY WARNING: don't run with debug turned on in production!
    settings.DEBUG = True
    settings.INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )
    settings.MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
    settings.INTERNAL_IPS = ('127.0.0.1',)
