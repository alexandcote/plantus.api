from django.conf.urls import (
    url,
    include
)
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from authentication.views import UserViewSet
from places.views import (
    PlaceViewSet,
)
from plantus.views import WelcomeView

router = SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^auth/token/', obtain_jwt_token, name='auth-token'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
