from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return IsAuthenticatedOrReadOnly
        return obj.author == request.user
