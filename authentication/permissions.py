from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated() and \
                   request.user.is_superuser
        elif view.action == 'create':
            return True
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update']:
            return request.user.is_authenticated() and \
                   (obj == request.user or request.user.is_superuser)
        elif view.action == 'destroy':
            return request.user.is_authenticated() and \
                   request.user.is_superuser
        else:
            return False
