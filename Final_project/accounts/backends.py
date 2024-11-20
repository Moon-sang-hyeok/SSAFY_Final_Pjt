from django.contrib.auth.backends import BaseBackend
from accounts.models import CustomUser

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
