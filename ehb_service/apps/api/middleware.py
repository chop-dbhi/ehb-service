import logging

from django.http import HttpResponseNotAllowed, HttpResponseForbidden

from .backends import TokenBackend
from .tokens import get_request_token
from django.conf import settings

log = logging.getLogger(__name__)

class TokenMiddleware(object):

    methods = ('OPTIONS', 'POST', 'GET', 'PUT', 'DELETE')

    preflight_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
    }

    def process_request(self, request):

        SITE_ALLOW = [
            settings.FORCE_SCRIPT_NAME + '/admin/'
        ]

        if getattr(request, 'user', None) and request.user.is_authenticated():
            return

        # Token-based authentication is attempting to be used, bypass CSRF
        # check
        key = get_request_token(request)
        if key:
            user = TokenBackend().authenticate(key)
            if user:
                request.user = user
                request.csrf_processing_done = True
                return
            else:
                log.warning(
                    'Invalid Request - Bad Key - from {0} with key {1}'.format(
                        request.META['REMOTE_ADDR'],
                        key
                    )
                )
                return HttpResponseForbidden('403 - Forbidden')
        if not request.user.is_authenticated() and request.path not in SITE_ALLOW:
            return HttpResponseForbidden('403 - Forbidden')

    def process_response(self, request, response, **kwargs):

        for k, v in self.preflight_headers.iteritems():
            response[k.title()] = v

        if request.method not in self.methods:
            log.warning(
                'Received bad request method from {0}'.format(
                    request.META['REMOTE_ADDR']
                )
            )
            return HttpResponseNotAllowed(self.methods)

        return response
