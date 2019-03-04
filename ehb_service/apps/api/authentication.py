from rest_framework import authentication
from rest_framework import exceptions
from api.models import ApiToken
from django.contrib.auth.models import User

class APITokenAuthentication(authentication.BaseAuthentication):
    'Custom authentication with api token model.'

    def authenticate(self, request):
        token = request.META.get('HTTP_API_TOKEN')
        if not token:
            return None
        try:
            apitoken = ApiToken.objects.get(token=token)
        except ApiToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token does not exist')
        userid = getattr(apitoken, 'user_id')
        user = User.objects.get(id=userid)
        return (user, None)
