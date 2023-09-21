from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # if isinstance(request.user, AnonymousUser):
        #     return False
        return request.user.is_staff
