from rest_framework import permissions


class PotsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        return user.is_authenticated and \
            (user.is_superuser or obj.place in user.places.all())
