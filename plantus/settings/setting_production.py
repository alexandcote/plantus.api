
def configure(settings):

    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

    settings.ALLOWED_HOSTS = ['plantus.xyz']