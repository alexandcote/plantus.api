from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.permissions import UserPermission
from authentication.serializers import UserSerializer
from places.serializers import SimplePlaceSerializer


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    @detail_route()
    def places(self, request, pk=None):
        users = self.get_object()
        serializer = SimplePlaceSerializer(users.places.all(), context={
            'request': request}, many=True)
        return Response(serializer.data)

    @list_route()
    def me(self, request):
        user = self.request.user
        data = UserSerializer(user, context={'request': request}).data
        return Response(data)
