
def configure(settings):

    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer'
    )
    settings.ALLOWED_HOSTS = ['api.plantus.xyz']
    settings.STATIC_ROOT = '/var/www/api.plantus.xyz/static/'

    settings.MEDIA_ROOT = '/var/www/api.plantus.xyz/media/'
    settings.MEDIA_URL = 'https://media.plantus.xyz/'

    # Celery configuration
    settings.CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
    settings.CELERY_TASK_ALWAYS_EAGER = False
    settings.CELERY_RESULT_BACKEND = 'django-db'

    # CORS configuration
    settings.CORS_ORIGIN_WHITELIST = ('plantus.xyz',)
