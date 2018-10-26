import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from api.helpers import FormHelpers
from constants import ErrorConstants
from core.models.identities import Subject, Organization, ExternalRecord
from core.forms import SubjectForm

log = logging.getLogger(__name__)


@permission_classes((permissions.AllowAny,))
class SubjectView (APIView):

    def _read_and_action(self, request, sfunc, **kwargs):
        pk = kwargs.pop("pk", None)
        orgpk = kwargs.pop("org_pk", None)
        org_sub_id = kwargs.pop("osid", None)
        external_sys = kwargs.pop("externalrecsys", None)
        external_id = kwargs.pop("erid", None)
        s = None

        if pk:
            try:
                s = Subject.objects.get(pk=pk)
            except Subject.DoesNotExist:
                log.error("Subject[{0}] not found".format(pk))
                return Response (status=status.HTTP_404_NOT_FOUND)

        # search for subjects based on their orginization and subj ID
        if orgpk and org_sub_id:
            try:
                org = Organization.objects.get(pk=orgpk)
                subs = Subject.objects.filter(organization=org).filter(organization_subject_id=org_sub_id)
                if subs.__len__() == 1:
                    s = subs[0]
                else:
                    log.error("Subject not found in Organization: {0} with provided Organization ID".format(org))
                    return Response ( status=status.HTTP_404_NOT_FOUND)
            except Organization.DoesNotExist:
                log.error("Subject not found. Given Organization does not exist")
                return Response (status=status.HTTP_404_NOT_FOUND)

        # search for subjects based on an external record id
        if external_sys and external_id:
            try:
                s = self.search_sub_by_external_record_id(external_sys, external_id)
                try:
                    if s.status_code == 404:
                        return Response (status=status.HTTP_404_NOT_FOUND)
                except:
                    'external record was found' #continue
            except Organization.DoesNotExist:
                log.error("Subject not found. Given External Record does not exist")
                return Response ( status=status.HTTP_404_NOT_FOUND)

        if s:
            return sfunc(s)

    def get(self, request, **kwargs):
        def onSuccess(s):
            r = s.responseFieldDict()
            return Response(r)
        return self._read_and_action(request, onSuccess, **kwargs)

    def delete(self, request, **kwargs):
        def onSuccess(s):
            s.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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
            return Response(response)

    def put(self, request):
        """This method is intended for updating an existing Subject record"""
        response = []

        for item in request.data:
            pkval = item.get('id')
            s = item.get('new_subject')

            if not pkval or not s:
                log.error("Unable to update Subject. No identifier provided")
                return Response(status=status.HTTP_400_BAD_REQUEST)
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
        return Response(response)

    def search_sub_by_external_record_id(self, external_sys, external_id):
        ex_record = ExternalRecord.objects.filter(external_system=external_sys).filter(record_id=external_id)
        if ex_record.__len__() != 1:
            log.error("External Record id {0} does not exist".format(ex_record))
            return Response(status=status.HTTP_404_NOT_FOUND)
        for s in ex_record:
            sub = s.subject.id
        s = Subject.objects.get(pk=sub)
        return s
