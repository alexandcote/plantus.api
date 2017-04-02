
def configure(settings):

    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer'
    )
    settings.ALLOWED_HOSTS = ['api.plantus.xyz']
    settings.STATIC_ROOT = '/var/www/plantus.xyz/static/'

    # CORS configuration
    settings.CORS_ORIGIN_WHITELIST = ('plantus.xyz',)
