from rest_framework import permissions


class PlacesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.user.is_authenticated and \
                (request.user.is_superuser or obj in user.places.all()):
            return True
        else:
            return False
