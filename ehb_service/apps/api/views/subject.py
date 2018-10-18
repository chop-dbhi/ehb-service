from django.http import HttpResponse
from restlib2.resources import Resource
from restlib2.http import codes

from api.helpers import FormHelpers
from constants import ErrorConstants
from core.models.identities import Subject, Organization, ExternalRecord
from core.forms import SubjectForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SubjectSerializer

log = logging.getLogger(__name__)
import sys

class SubjectResource (APIView):
# class SubjectResource(Resource):
    # print ("we are in subject resource")
    # print sys._getframe().f_back.f_code.co_name

    def get (self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer (subjects, many=True)
        return Response(serializer.data)



    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.Subject'

    def _read_and_action(self, request, sfunc, **kwargs):
        print ("we are in read and action")
        print ("this is sfunc")
        print (sfunc)
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
                return HttpResponse(status=codes.not_found)

        # search for subjects based on their orginization and subj ID
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

        # search for subjects based on an external record id
        if external_sys and external_id:
            try:
                s = self.search_sub_by_external_record_id(external_sys, external_id)
            except Organization.DoesNotExist:
                log.error("Subject not found. Given External Record does not exist")
                return HttpResponse(status=codes.not_found)

        if s:
            return sfunc(s)

    def get(self, request, **kwargs):
        def onSuccess(s):
            r = s.responseFieldDict()
            print (r)
            return json.dumps(r)
        return self._read_and_action(request, onSuccess, **kwargs)

    def delete(self, request, **kwargs):
        def onSuccess(s):
            s.delete()
            return HttpResponse(status=codes.ok)
        return self._read_and_action(request, onSuccess, **kwargs)

    def post(self, request):
        print ("we are in post")
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

    def search_sub_by_external_record_id(self, external_sys, external_id):
        ex_record = ExternalRecord.objects.filter(external_system=external_sys).filter(record_id=external_id)
        if ex_record.__len__() != 1:
            log.error("External Record id {0} does not exist".format(ex_record))
            return HttpResponse(status=codes.not_found)
        for s in ex_record:
            sub = s.subject.id
        s = Subject.objects.get(pk=sub)
        return s