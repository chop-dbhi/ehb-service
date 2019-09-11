import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from api.helpers import FormHelpers
from .constants import ErrorConstants
from core.models.identities import Subject, Organization, ExternalRecord
from core.forms import UserAuditForm

log = logging.getLogger(__name__)


class UserAuditView (APIView):
    def post(self, request):
        response = []

        form = UserAuditForm(request.data)
        FormHelpers.processFormJsonResponse(form, response)
        return Response(response)
