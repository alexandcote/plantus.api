import uuid

from rest_framework import permissions

from places.models import Place


class PotsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or \
               obj.place in request.user.places.all()


class TimeSeriesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action is'create':
            identifier = request.META.get('HTTP_X_AUTHORIZATION', '')

            try:
                identifier = uuid.UUID(identifier)
                return Place.objects.filter(identifier=identifier).exists()
            except ValueError:
                return False

        elif view.action in ['destroy', 'update', 'partial_update']:
            return False
        elif view.action in ['list', 'retrieve']:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or \
               obj.pot.place in request.user.places.all()


class OperationsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action is'create':
            return request.user.is_authenticated
        elif view.action in ['destroy', 'update', 'partial_up']:
            return False
        elif view.action in ['list', 'retrieve']:
            identifier = request.META.get('HTTP_X_AUTHORIZATION', '')
            try:
                identifier = uuid.UUID(identifier)
                return Place.objects.filter(identifier=identifier).exists()
            except ValueError:
                return request.user.is_authenticated
        elif view.action == 'completed':
            identifier = request.META.get('HTTP_X_AUTHORIZATION', '')
            try:
                identifier = uuid.UUID(identifier)
                return Place.objects.filter(identifier=identifier).exists()
            except ValueError:
                return request.user.is_authenticated and \
                       request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            identifier = request.META.get('HTTP_X_AUTHORIZATION', '')
            try:
                identifier = uuid.UUID(identifier)
                place = Place.objects.filter(identifier=identifier)
                return obj.pot.place in place
            except ValueError:
                return False
        else:
            return request.user.is_superuser or \
               obj.pot.place in request.user.places.all()
