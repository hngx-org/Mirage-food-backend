from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # if isinstance(request.user, AnonymousUser):
        #     return False
        return request.user.is_staff

class isOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
