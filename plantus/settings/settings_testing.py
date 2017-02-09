
def configure(settings):
    settings.INSTALLED_APPS += ('django_nose',)
    settings.TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)

    settings.NOSE_ARGS = (
        '--cover-package=plantus,authentication,places,plants',
        '--cover-inclusive',
    )