
def configure(settings):
    # SECURITY WARNING: don't run with debug turned on in production!
    settings.DEBUG = True
    settings.INSTALLED_APPS += (
        'debug_toolbar',
    )
    settings.MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

    settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
    settings.INTERNAL_IPS = ('127.0.0.1',)
