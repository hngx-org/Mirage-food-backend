from django.contrib.auth.backends import ModelBackend
from .models import User
import logging


class CustomBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists ")
            return None
        except Exception as e:
            logging.getLogger('error_logger').error(repr(e))

    
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None
