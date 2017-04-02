from django.db.models import Q
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.permissions import UserPermission
from authentication.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_fields = ('places',)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_superuser:
            queryset = User.objects\
                .filter(Q(places__in=user.places.all()) | Q(id=user.id))\
                .distinct()\
                .order_by('last_name', 'first_name')

        return queryset

    @list_route()
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
