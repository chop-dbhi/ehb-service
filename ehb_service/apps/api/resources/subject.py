import json
import logging

from django.http import HttpResponse
from restlib2.resources import Resource
from restlib2.http import codes

from api.helpers import FormHelpers
from constants import ErrorConstants
from core.models.identities import Subject, Organization
from core.forms import SubjectForm

log = logging.getLogger(__name__)


class SubjectResource(Resource):
    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.Subject'

    def _read_and_action(self, request, sfunc, **kwargs):
        pk = kwargs.pop("pk", None)
        orgpk = kwargs.pop("org_pk", None)
        org_sub_id = kwargs.pop("osid", None)
        s = None

        if pk:
            try:
                s = Subject.objects.get(pk=pk)
            except Subject.DoesNotExist:
                log.error("Subject[{0}] not found".format(pk))
                return HttpResponse(status=codes.not_found)

        if orgpk and org_sub_id:
            try:
                org = Organization.objects.get(pk=orgpk)
                subs = Subject.objects.filter(organization=org).filter(organization_subject_id=org_sub_id)
                if subs.__len__() == 1:
                    s = subs[0]
                else:
                    log.error("Subject not found in Organization: {0} with provided Organization ID".format(org))
                    return HttpResponse(status=codes.not_found)
            except Organization.DoesNotExist:
                log.error("Subject not found. Given Organization does not exist")
                return HttpResponse(status=codes.not_found)

        if s:
            return sfunc(s)

    def get(self, request, **kwargs):
<<<<<<< HEAD
=======
        print "we're in get"
>>>>>>> 3e7c48e... added api.rst file
        def onSuccess(s):
            r = s.responseFieldDict()
            return json.dumps(r)
        return self._read_and_action(request, onSuccess, **kwargs)

    def delete(self, request, **kwargs):
        def onSuccess(s):
            s.delete()
            return HttpResponse(status=codes.ok)
        return self._read_and_action(request, onSuccess, **kwargs)

    def post(self, request):
        """This method is intended for adding new Subject records"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for s in request.data:
                form = SubjectForm(s)
                args = {
                    'organization_subject_id': s.get('organization_subject_id'),
                    'organization_id': s.get('organization')
                }
                FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)

            return json.dumps(response)

    def put(self, request):
        """This method is intended for updating an existing Subject record"""
        response = []

        for item in request.data:
            pkval = item.get('id')
            s = item.get('new_subject')

            if not pkval or not s:
                log.error("Unable to update Subject. No identifier provided")
                return HttpResponse(status=codes.bad_request)
            try:
                subj = Subject.objects.get(pk=pkval)
                fn = s.get('first_name', subj.first_name)
                ln = s.get('last_name', subj.last_name)
                orgid = s.get('organization', subj.organization)
                org_sub_id = s.get('organization_subject_id', subj.organization_subject_id)
                dob = s.get('dob', subj.dob)
                js = {
                    "first_name": fn,
                    "last_name": ln,
                    "organization": orgid,
                    "organization_subject_id": org_sub_id,
                    "dob": dob
                }
                form = SubjectForm(js, instance=subj)
                FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})
            except Subject.DoesNotExist:
                log.error("Unable to update Subject. Subject[{0}] does not exist".format(pkval))
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
