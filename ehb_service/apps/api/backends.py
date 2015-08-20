import logging

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .tokens import token_generator
from .models import ApiToken

log = logging.getLogger(__name__)

class TokenBackend(ModelBackend):
    def authenticate(self, token):
        # For backwards compatibility only use the ApiToken model if
        # Serrano is installed as an app as this was not a requirement
        # previously.
        try:
            token = ApiToken.objects.get_active_token(token)
            return token.user
        except ApiToken.DoesNotExist:
            log.error("Unable to authenticate token provided [{0}] does not exist.".format(token))
            pass

        pk, token = token_generator.split(token)

        try:
            pk = int(pk)
        except (ValueError, TypeError):
            log.error("Unable to generate token")
            return

        try:
            user = User.objects.get(pk=pk, is_active=True)
        except User.DoesNotExist:
            log.error("Unable to authenticate. User[{0}] does not exist".format(pk))
            return

        if token_generator.check(user, token):
            return user
