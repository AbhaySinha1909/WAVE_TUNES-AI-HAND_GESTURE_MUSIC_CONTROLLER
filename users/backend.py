from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(BaseBackend):
    """
    Custom Authentication Backend
    Allows users to log in using EMAIL instead of username.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        try:
            # Check if a user exists with this email (case insensitive)
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None

        # Check password
        if user.check_password(password):
            return user
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

