from . import models

<<<<<<< HEAD

=======
>>>>>>> 61f328dee497fbcbfd352ac01075f5d666a17e4b
class Organization:
    @staticmethod
    def create_organization(name: str, lunch_price: float, currency: str) -> "Organization":
        return models.Organization.objects.create(
            name=name, lunch_price=lunch_price, currency=currency
        )
