from rest_framework import permissions


class PlantPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['destroy', 'update', 'partial_update', 'create']:
            return request.user.is_authenticated() and \
                   request.user.is_superuser
        return True
