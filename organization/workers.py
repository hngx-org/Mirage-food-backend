from . import models


class Organization:
    @staticmethod
    def create_organization(name: str, lunch_price: float, currency: str) -> "Organization":
        return models.Organization.objects.create(
            name=name, lunch_price=lunch_price, currency=currency
        )
