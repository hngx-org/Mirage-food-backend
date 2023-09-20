from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.views import APIView

from users.serializers import UserSerializer

from .models import OrganizationInvites
from .serializers import ListInvitesSerializer
from .permissions import OrganisationAdmin


class ListInvitesView(APIView):
    """
    If user is an admin this lists all the invites in their Organisation
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [OrganisationAdmin]

    def get(self, request):
        user = request.user
        invites = OrganizationInvites.objects.filter(org_id=user.org_id)
        return Response(ListInvitesSerializer(invites).data)
