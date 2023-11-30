from django.contrib.auth.models import User
from registration_app.models import Profile


class EmailAuthBackend:
    """
    Authenticate by email
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def create_profile(backend, user, *args, **kwargs):
    """
    Create profile for social auth
    """
    Profile.objects.get_or_create(user=user)