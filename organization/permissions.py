from rest_framework import permissions


class OrganisationAdmin(permissions.BasePermission):
    """
    Check if user is an admin of an organisation.
    """

    def has_permission(self, request, view):
        return (request.user and request.user.is_admin)
