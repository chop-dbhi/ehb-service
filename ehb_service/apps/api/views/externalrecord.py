import json
import logging

from django.db.models import Q
from core.forms import ExternalRecordForm, ExternalRecordRelationForm
from constants import ErrorConstants
from api.helpers import FormHelpers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from core.models.identities import ExternalRecord, \
    ExternalRecordRelation, ExternalRecordLabel, Subject, ExternalSystem

log = logging.getLogger(__name__)

class ExternalRecordQuery(APIView):

    def responseLabels(self, subjid, subj_org, subj_org_id, esid, esname, esurl, path):

        label_dict = {}

        # Subject based labels
        if subjid:
            label_dict['subject_id'] = subjid
        elif subj_org and subj_org_id:
            label_dict['subject_org'] = subj_org
            label_dict['subject_org_id'] = subj_org_id
        else:
            label_dict['subject_'] = 'not_provided'

        # External system based labels
        if esid:
            label_dict['external_system_id'] = esid
        elif esname:
            label_dict['external_system_name'] = esname
        elif esurl:
            label_dict['external_system_url'] = esurl
        else:
            label_dict['external_system_'] = 'not_provided'

        # Path modifiers
        if path:
            label_dict['path'] = path
        else:
            label_dict['path_'] = 'not_provided'

        return label_dict

    def appendError(self, response, errormsg, subjid, subj_org, subj_org_id, esid, esname, esurl, path):
        response_dict = self.responseLabels(subjid, subj_org, subj_org_id, esid, esname, esurl, path)
        response_dict['errors'] = errormsg
        response.append(response_dict)

    def post(self, request):
        """
        This method is intended for querying for ExternalRecord records.
        The query can be on any combination of Subject, ExternalSystem and path.
        It is not necessary to specify all 3, but at least 1 must be provided.
        The Subject can be specified by supplying the subject_id OR the subject_org AND subject_org_id.
        The ExternalSystem can be specified by supplying the external_system_id OR external_system_name OR external_system_url
        The path can be specified by supplying the path. This is the path to the record collection on the external system
        """

        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for s in request.data:

                # Look for valid subject and externalSystem identifiers
                subjid = s.get('subject_id')
                subj_org = s.get('subject_org')
                subj_org_id = s.get('subject_org_id')
                esid = s.get('external_system_id')
                esname = s.get('external_system_name')
                esurl = s.get('external_system_url')
                subj = None
                es = None
                path = s.get('path')

                # try to query for Subject, External System
                try:

                    if subjid:
                        subj = Subject.objects.get(pk=subjid)
                    elif subj_org and subj_org_id:
                        qs = Subject.objects.filter(organization=subj_org).filter(organization_subject_id=subj_org_id)
                        if qs.__len__() == 1:
                            subj = qs[0]

                    if esid:
                        es = ExternalSystem.objects.get(pk=esid)
                    elif esname:
                        es = ExternalSystem.objects.get(name=esname)
                    elif esurl:
                        es = ExternalSystem.objects.get(url=esurl)

                    # Try to query for ExternalRecords
                    ers = ExternalRecord.objects.all()

                    if subj:
                        ers = ers.filter(subject__pk=str(subj.pk))
                    if es:
                        ers = ers.filter(external_system__pk=str(es.pk))
                    if path:
                        ers = ers.filter(path=path)
                    if ers:
                        era = []
                        for er in ers:
                            era.append(er.responseFieldDict())
                        response_dict = self.responseLabels(subjid, subj_org, subj_org_id, esid, esname, esurl, path)
                        response_dict['external_record'] = era
                        response.append(response_dict)
                    else:
                        log.error("No ExternalRecord found for query.")
                        response.append({"errors": [{"Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY}]})
                except Subject.DoesNotExist:
                    log.error("No ExternalRecord found. Subject does not exist")
                    self.appendError(
                        response,
                        {
                            "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
                        },
                        subjid,
                        subj_org,
                        subj_org_id,
                        esid,
                        esname,
                        esurl,
                        path
                    )
                except ExternalSystem.DoesNotExist:
                    log.error("No ExternalRecord found. External System does not exist")
                    self.appendError(
                        response,
                        {
                            "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
                        },
                        subjid,
                        subj_org,
                        subj_org_id,
                        esid,
                        esname,
                        esurl,
                        path
                    )

            return Response(response)

class ExternalRecordView(APIView):

    supported_accept_types = ['application/json', 'application/xml']

    model = 'core.models.identities.ExternalRecord'

    def get(self, request, pk):
        er = None
        try:
            er = ExternalRecord.objects.get(pk=pk)
        except ExternalRecord.DoesNotExist:
            log.error("Unable to retrieve ExternalRecord[{0}]. It does not exists.".format(pk))
            return Response(status=status.HTTP_404_NOT_FOUND)
        if er:
            r = er.responseFieldDict()

            return Response (r)

    def post(self, request):
        """This method is intended for adding new ExternalRecord records"""

        content_type = request.META.get("CONTENT_TYPE")

        response = []

        if content_type == "application/json":

            for s in request.data:
                label = s.get('label_id')
                recordid = s.get('record_id')
                path = s.get('path')
                form = ExternalRecordForm(s)
                args = {'record_id': recordid}

                if path:
                    args['path'] = path

                if label:
                    args['label_id'] = int(label)
                else:
                    args['label_id'] = 1

                FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)

            return Response(response)

    def put(self, request):
        """This method is intended for updating an existing ExternalRecord record"""

        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for item in request.data:

                pkval = item.get('id')
                s = item.get('external_record')

                if not pkval or not s:
                    log.error("Unable to update existing ExternalRecord no identifier provided")
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                try:
                    er = ExternalRecord.objects.get(pk=pkval)
                    subjid = s.get('subject', str(er.subject.pk))
                    esid = s.get('external_system', str(er.external_system.pk))
                    erri = s.get('record_id', er.record_id)
                    erpath = s.get('path', er.path)

                    if er.label:
                        label = s.get('label', er.label.id)
                    else:
                        label = s.get('label')

                    js = {
                        "subject": subjid,
                        "external_system": esid,
                        "record_id": erri,
                        "path": erpath,
                        "label": label
                    }
                    form = ExternalRecordForm(js, instance=er)

                    FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})

                except ExternalRecord.DoesNotExist:
                    log.error("Unable to update ExternalRecord. ExternalRecord not found")
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

    def delete(self, request, pk):
        try:
            er = ExternalRecord.objects.get(pk=pk)
            er.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ExternalRecord.DoesNotExist:
            log.error("Unable to delete ExternalRecord as it does not exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class ExternalRecordLabelView(APIView):
    '''
    Provide a View to provide ExternalRecord labels.
    '''
    supported_accept_type = ['application/json']
    model = 'core.models.identities.ExternalRecordLabel'

    def get(self, request, pk):
        try:
            erl = ExternalRecordLabel.objects.get(pk=pk)
            return json.dumps({"id": erl.id, "label": erl.label})
        except ExternalRecordLabel.DoesNotExist:
            log.error("Unable to retrieve ExternalRecord label. Label not found.")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        response = []
        labels = ExternalRecordLabel.objects.all()
        for label in labels:
            response.append({
                "id": label.id,
                "label": label.label
            })
        return Response(response)

class ExternalRecordRelationView(APIView):
    '''
    Provide a View to provide related ExternalRecords.
    '''
    def get(self, request, pk, link=None):

        response = []
        if link:
            relations = ExternalRecordRelation.objects.filter(external_record=pk, pk=link)
        else:
            relations = ExternalRecordRelation.objects.filter(Q(external_record=pk) | Q(related_record=pk))

        data = []
        for relation in relations:
            r = relation.to_dict()
            primary = False
            if int(pk) == r['external_record']['id']:
                primary = True
            d = {
                'external_record': r['related_record'],
                'type': r['type'],
                'description': r['relation_description'],
                'id': r['id'],
                'primary': primary
            }
            if (r['related_record']['id'] == int(pk)):
                d['external_record'] = r['external_record']
            data.append(d)
        if link:
            return Response(data[0])
        else:
            return Response(data)

    def post(self, request, pk):
        '''
        This method is intended for adding new ExternalRecordRelation records
        {
            "related_record": 2,
            "relation_type": 1
        }
        '''

        content_type = request.META.get("CONTENT_TYPE")

        response = []

        if content_type == "application/json":
            s = request.data
            s['external_record'] = pk
            # Check if this already exists
            args = {}
            args['external_record'] = request.data.get('external_record')
            args['related_record'] = request.data.get('related_record')
            args['relation_type'] = request.data.get('relation_type')
            if len(ExternalRecordRelation.objects.filter(external_record=args['external_record'], related_record=args['related_record'], relation_type=args['relation_type'])) > 0:
                return json.dumps({'success': False, 'error': 'Record relation already exists'})
            form = ExternalRecordRelationForm(s)
            r = FormHelpers.processFormJsonResponse(form, response, invalid_dict=args, valid_dict=args)

            return Response(r)

    def delete(self, request, pk, link):
        '''
        This method deletes the specified ExternalRecordRelation based id passed
        via the URL
        '''

        response = []
        try:
            record = ExternalRecordRelation.objects.get(pk=link)
            record.delete()
            response.append(
                {
                    "success": True
                }
            )
        except ExternalRecordRelation.DoesNotExist:
            response.append(
                {
                    'error': 'Record relation does not exist',
                    'success': False
                }
            )
        return Response(response)
