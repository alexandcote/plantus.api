from django.conf.urls import (
    url,
    include
)
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from authentication.views import UserViewSet
from places.views import (
    PlaceViewSet,
)
from plants.views import PlantViewSet
from plantus.settings.settings_share import PLANTUS_ENV
from plantus.views import WelcomeView
from pots.views import (
    PotViewSet,
    TimeSeriesViewSet,
    OperationsViewSet)

router = SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'plants', PlantViewSet)
router.register(r'pots', PotViewSet)
router.register(r'timeseries', TimeSeriesViewSet)
router.register(r'operations', OperationsViewSet)

urlpatterns = [
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^auth/token/', obtain_jwt_token, name='auth-token'),
    url(r'^', include(router.urls)),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
)

if PLANTUS_ENV == 'development':
    import debug_toolbar
    from django.conf.urls.static import static
    from plantus.settings.settings_share import (
        MEDIA_URL,
        MEDIA_ROOT
    )
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)

if PLANTUS_ENV in ['development', 'staging']:
    urlpatterns += [
        url(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework')),
    ]
