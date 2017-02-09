from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.permissions import UserPermission
from authentication.serializers import UserSerializer
from places.serializers import PlaceSerializer


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    @detail_route()
    def places(self, request, pk=None):
        user = self.get_object()
        serializer = PlaceSerializer(user.places.all(), context={
            'request': request}, many=True)
        return Response(serializer.data)

    @list_route()
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
