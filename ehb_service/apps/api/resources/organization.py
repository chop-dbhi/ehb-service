import json
import logging

from restlib2.resources import Resource
from restlib2.http import codes
from django.http import HttpResponse

from api.helpers import FormHelpers
from constants import ErrorConstants
from core.models.identities import Organization
from core.forms import OrganizationForm

log = logging.getLogger(__name__)

class OrganizationQuery(Resource):
    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.Organization'

    def post(self, request):
        """This method is intended querying for Organization records by name"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for o in request.data:
                nameval = o.get('name')

                if nameval:
                    try:
                        org = Organization.objects.get(name=nameval)
                        response.append(
                            {
                                "name": nameval,
                                "organization": org.responseFieldDict()
                            }
                        )
                    except Organization.DoesNotExist:
                        log.error("Organization does not exist")
                        response.append(
                            {
                                "name": nameval,
                                "errors": [
                                    {
                                        "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
                                    }
                                ]
                            }
                        )
                else:
                    log.error("No Organization found. Invalid query")
                    response.append(
                        {
                            "errors": [
                                {
                                    "Query": ErrorConstants.ERROR_INVALID_QUERY
                                }
                            ]
                        }
                    )

            return json.dumps(response)


class OrganizationResource(Resource):
    supported_accept_types = ['application/json']
    model = 'core.models.identities.Organization'

    def _read_and_action(self, request, func, **kwargs):
        pk = kwargs.pop("pk")
        org = None

        if pk:
            try:
                org = Organization.objects.get(pk=pk)
            except Organization.DoesNotExist:
                log.error("Organization not found")
                return HttpResponse(status=codes.not_found)
            return func(org)

    def get(self, request, **kwargs):
        def onSuccess(org):
            r = org.responseFieldDict()
            return json.dumps(r)

        return self._read_and_action(request, onSuccess, **kwargs)

    def delete(self, request, **kwargs):
        def onSuccess(org):
            org.delete()
            return HttpResponse(status=codes.ok)
        return self._read_and_action(request, onSuccess, **kwargs)

    def post(self, request):
        """This method is intended for adding new Organization records"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []
        if content_type == "application/json":
            for org in request.data:
                name = org.get('name')
                form = OrganizationForm(org)
                args = {'name': name}
                FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)
            return json.dumps(response)

    def put(self, request, **kwargs):
        """This method is intended for updating an existing Organization record"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for item in request.data:
                pkval = item.get('id')
                if not pkval:
                    log.error('Unable to update Organization. No identifier provided')
                    return HttpResponse(status=codes.unprocessable_entity)
                try:
                    org = Organization.objects.get(pk=int(pkval))
                    n = item.get('name', org.name)
                    label = item.get('subject_id_label', org.subject_id_label)
                    js = {"name": n, "subject_id_label": label}
                    form = OrganizationForm(js, instance=org)
                    FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})
                except Organization.DoesNotExist:
                    log.error("Organization[{0}] does not exist.".format(pkval))
                    response.append(
                        {
                            'id': pkval,
                            'success': False,
                            'errors': [
                                {
                                    'id': ErrorConstants.ERROR_RECORD_ID_NOT_FOUND
                                }
                            ]
                        }
                    )

            return json.dumps(response)