from django.contrib.auth.backends import ModelBackend as _ModelBackend
from django.contrib.auth.models import User

from towel.mt import access_model, client_model


class ModelBackend(_ModelBackend):
    """
    Custom authentication backend for Keetab

    This authentication backend serves two purposes:

    1. Allowing e-mail addresses as usernames (``authenticate``)
    2. Minimizing DB accesses by fetching additional information about the
       current user earlier (``get_user``)
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        Access = access_model()
        Client = client_model()
        try:
            access = Access.objects.select_related(
                'user',
                Client.__name__.lower(),
                ).get(user=user_id)

            # Ensure reverse accesses do not needlessly query the DB again.
            # Maybe Django already does that for us already... whatever.
            setattr(access.user, User.access.cache_name, access)
            return access.user
        except Access.DoesNotExist:
            pass

        try:
            # Fall back to raw user access
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

        return None
