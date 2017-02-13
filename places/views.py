from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.serializers import UserSerializer
from places.models import Place
from places.permissions import PlacesPermission
from places.serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing places.
    """
    queryset = Place.objects.prefetch_related('users').all()
    permission_classes = [PlacesPermission]
    serializer_class = PlaceSerializer
    page_size = 3

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not request.user.is_superuser:
            queryset = queryset.filter(users=request.user)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @detail_route()
    def users(self, request, pk=None):
        place = self.get_object()
        queryset = place.users.prefetch_related('places').all()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = UserSerializer(page, context={
                'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, context={
            'request': request}, many=True)

        return Response(serializer.data)
