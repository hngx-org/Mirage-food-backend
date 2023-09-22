import random
import string

from django.core.mail import send_mail


def send_organization_invite_mail(
    from_email: str,
    to_email: str,
    organization_name: str,
    token: str = "",
) -> bool:
    subject = f"Invite from {organization_name}"
    message = f"Here is your token:  {token}\n\nThis token will grant you access to all the features and benefits on our platform. Should you require any assistance or have questions, please feel free to reach out to our support team.{comment}"
    sent = send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
    )
    if sent == 1:
        return True
    return False


def generate_random_token(length):
    # Define the character pool for the token
    characters = (
        string.ascii_letters + string.digits
    )  # Uppercase letters, lowercase letters, and numbers
    # Generate a random token by selecting characters randomly from the pool
    token = "".join(random.choice(characters) for _ in range(length))
    return token
