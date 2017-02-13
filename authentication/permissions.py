from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif view.action in ['list', 'destroy']:
            return request.user.is_authenticated() and \
                   request.user.is_superuser
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated() and \
               (obj == request.user or request.user.is_superuser)
