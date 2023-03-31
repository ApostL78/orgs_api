from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have same id with user
        return obj.id == request.user.id


class IsAuthenticatedOrPostAndReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only + post request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ("GET", "HEAD", "OPTIONS", "POST")
            or request.user
            and request.user.is_authenticated
        )
