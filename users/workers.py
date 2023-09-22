from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()
class UserWorker:

    @staticmethod
    def get_user_details(user_id):
        """Returns user details: name, emal, profile picture url"""
        user = get_object_or_404(User, pk=user_id)
        user_details = {
            "user_id": user.id,
            "name": user.first_name + " " + user.last_name,
            "email": user.email,
            "profile_picture": user.profile_pic.url
        }
        return user_details
