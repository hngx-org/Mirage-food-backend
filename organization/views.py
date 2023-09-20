from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from .models import OrganizationInvites
from .serializers import ListInvitesSerializer
from .permissions import OrganisationAdmin


class AllInvites(generics.ListAPIView):
    permission_classes = [OrganisationAdmin]
    queryset = OrganizationInvites.objects.all()
    serializer_class = ListInvitesSerializer

    def get_queryset(self, org_pk=None):
        invites = OrganizationInvites.objects.filter(org_pk=org_pk)
        return invites

    def get(self, request, user_pk=None, org_pk=None):
        print(request.user)
        queryset = self.get_queryset(org_pk)
        serializePost = OrganizationInvites(queryset, many=True)
        return Response(serializePost.data)
