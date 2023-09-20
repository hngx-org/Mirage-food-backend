from rest_framework import generics, viewsets

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationAPI(generics.UpdateAPIView, viewsets.GenericViewSet):
    """Base view for organization update (put | patch)"""  # can be modified when adding other methods

    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.all()

    ...
