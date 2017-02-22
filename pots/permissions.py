from rest_framework import permissions


class PotsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or \
               obj.place in request.user.places.all()


class TimeSeriesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy', 'update', 'partial_update', 'create']:
            return request.user.is_authenticated() and \
                   request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or \
               obj.place in request.user.places.all()
