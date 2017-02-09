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
from plantus.views import WelcomeView

router = SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'plants', PlantViewSet)

urlpatterns = [
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^auth/token/', obtain_jwt_token, name='auth-token'),
    url(r'^', include(router.urls)),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
)
