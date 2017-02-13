from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.permissions import UserPermission
from authentication.serializers import UserSerializer
from places.serializers import PlaceSerializer
from pots.models import Pot
from pots.serializers import PotSerializer


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing users.
    """
    queryset = User.objects.prefetch_related('places').all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    @detail_route()
    def places(self, request, pk=None):
        user = self.get_object()
        queryset = user.places.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PlaceSerializer(page, context={
                'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PlaceSerializer(queryset, context={
            'request': request}, many=True)

        return Response(serializer.data)

    @detail_route()
    def pots(self, request, pk=None):
        user = self.get_object()
        places = user.places.all()
        queryset = Pot.objects.filter(place__in=places).all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PotSerializer(page, context={
                'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PotSerializer(queryset, context={
            'request': request}, many=True)

        return Response(serializer.data)

    @list_route()
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
