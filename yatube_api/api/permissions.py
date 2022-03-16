from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        return False


class OwnerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (obj.user == request.user
                and obj.user != obj.following):
            return True
        return False
