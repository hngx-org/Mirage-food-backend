from . import models
from . import helpers

class Organization:
    @staticmethod
    def create_organization(name: str, lunch_price: float, currency: str) -> "Organization":
        return models.Organization.objects.create(
            name=name, lunch_price=lunch_price, currency=currency
        )
    
    @staticmethod
    def create_organization_invite(admin_user, to_email):
        organization = admin_user.org_id
        token = helpers.generate_random_token(length=20)
        models.OrganizationInvites.objects.create(
            org_id=organization, email=to_email, token=token
        )
        sent = helpers.send_organization_invite_mail(
            from_email=admin_user.email, to_email=to_email, token=token, organization_name=organization.name
        )
        return sent
