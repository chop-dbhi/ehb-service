import json
import logging

from restlib2.resources import Resource
from restlib2.http import codes
from django.http import HttpResponse

from api.helpers import FormHelpers
from constants import ErrorConstants
from core.models.identities import ExternalSystem, ExternalRecord, Organization
from core.forms import ExternalSystemForm

log = logging.getLogger(__name__)

class ExternalSystemCrossReference(Resource):
    supported_accept_types = ['application/json']
    model = 'core.models.identities.ExternalSystem'

    class Meta(object):
        abstract = True

    def _read_and_action(self, request, func, pk):
        '''
        This method attempts to find an ExternalSystem object given the pk. If found it
        submits it to func for processing. This function is expected to operate on the
        response list object which is then returned by this function'''
        es = None
        try:
            es = ExternalSystem.objects.get(pk=pk)
        except ExternalSystem.DoesNotExist:
            log.error("ExternalSystem[{0}] not found".format(pk))
            return HttpResponse(status=codes.not_found)
        if es:
            response = []
            func(es, response)
            return json.dumps(response)

    def getOrganization(self, org_id):
        org = None
        if org_id:
            org = Organization.objects.get(pk=org_id)
        return org


class ExternalSystemRecords(ExternalSystemCrossReference):

    def get(self, request, pk, **kwargs):
        '''
        This resource provides a response with all of the external records that are
        associated with this external system. If the org_pk is provided,
        then only external records whos subject record belong to the organization
        will be returned. If the path is provide only external records with the
        path will be included
        '''

        try:
            org = self.getOrganization(kwargs.pop('org_pk', None))
        except Organization.DoesNotExist:
            log.error("Unable to retrieve ExternalSystemRecords. Organization not found")
            return HttpResponse(status=codes.not_found)

        def process(es, response):
            qs = ExternalRecord.objects.filter(external_system=es)

            if org:
                qs = qs.filter(subject__organization=org)

            for er in qs:
                r = er.responseFieldDict()
                response.append(r)

        return self._read_and_action(request, process, pk)


class ExternalSystemSubjects(ExternalSystemCrossReference):

    def get(self, request, pk, **kwargs):
        '''
        This resource provides a response with all of the subjects that have
        records associated with this external system. If the org_pk is provided,
        then only subject records that belong to this organization will be returned
        '''
        try:
            org = self.getOrganization(kwargs.pop('org_pk', None))
        except Organization.DoesNotExist:
            log.error("Unable to retrieve ExternalSystemSubjects. Organization not found")
            return HttpResponse(status=codes.not_found)

        def process(es, response):
            if not org:
                qs = es.subjects.all().distinct()
            else:
                qs = es.subjects.filter(organization=org).distinct()
            for s in qs:
                r = s.responseFieldDict()
                response.append(r)

        return self._read_and_action(request, process, pk)


class ExternalSystemQuery(Resource):

    supported_accept_types = ['application/json']
    model = 'core.models.identities.ExternalSystem'

    def post(self, request):
        """This method is intended querying for ExternalSystem records by name"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for s in request.data:
                nameval = s.get('name')
                urlval = s.get('url')

                if nameval:
                    try:
                        es = ExternalSystem.objects.get(name=nameval)
                        response.append(
                            {
                                "name": nameval,
                                "externalSystem":
                                es.responseFieldDict()
                            }
                        )
                    except ExternalSystem.DoesNotExist:
                        log.error("Unable to query for ExternalSystem no record found")
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
                elif urlval:
                    try:
                        es = ExternalSystem.objects.get(url=urlval)
                        response.append(
                            {
                                "url": urlval,
                                "externalSystem": es.responseFieldDict()
                            }
                        )
                    except ExternalSystem.DoesNotExist:
                        log.error("Unable to query for ExternalSystem no record found")
                        response.append(
                            {
                                "url": urlval,
                                "errors": [
                                    {
                                        "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
                                    }
                                ]
                            }
                        )
                else:
                    log.error("Unable to query for ExternalSystem. Invalid query")
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


class ExternalSystemResource(Resource):

    supported_accept_types = ['application/json']
    model = 'core.models.identities.ExternalSystem'

    def get(self, request, pk):
        es = None

        try:
            es = ExternalSystem.objects.get(pk=pk)
        except ExternalSystem.DoesNotExist:
            log.error("ExternalSystem[{0}] not found".format(pk))
            return HttpResponse(status=codes.not_found)

        r = es.responseFieldDict()

        return json.dumps(r)

    def post(self, request):
        """This method is intended for adding new ExternalSystem records"""

        response = []

        for s in request.data:
            name = s.get('name')
            form = ExternalSystemForm(s)
            args = {'name': name}

            FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)

        return json.dumps(response)

    def put(self, request):
        """This method is intended for updating an existing ExternalSystem record"""

        response = []

        for item in request.data:
            pkval = item.get('id')
            s = item.get('external_system')

            if not pkval or not s:
                log.error("Unable to update ExternalSystem. Identifier not provided")
                return HttpResponse(status=codes.bad_request)

            try:
                es = ExternalSystem.objects.get(pk=pkval)
                name = s.get('name', es.name)
                desc = s.get('description', es.description)
                url = s.get('url', es.url)
                js = {"name": name, "description": desc, "url": url}
                form = ExternalSystemForm(js, instance=es)
                FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})
            except ExternalSystem.DoesNotExist:
                log.error("Unable to update ExternalSystem. ExternalSystem[{0}] not found".format(pkval))
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

    def delete(self, request, pk):
        try:
            es = ExternalSystem.objects.get(pk=pk)
            es.delete()
            return HttpResponse(status=codes.ok)
        except ExternalSystem.DoesNotExist:
            log.error("Unable to delete ExternalSystem. ExternalSystem[{0}] no found".format(pk))
            return HttpResponse(status=codes.not_found)






# import json
# import logging
#
# # from restlib2.resources import Resource
# # from restlib2.http import codes
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import permission_classes
# from rest_framework import permissions
# from api.serializers import ExternalSystemSerializer
# from django.http import HttpResponse
#
# from api.helpers import FormHelpers
# from constants import ErrorConstants
# from core.models.identities import ExternalSystem, ExternalRecord, Organization
# from core.forms import ExternalSystemForm
#
# log = logging.getLogger(__name__)
#
# @permission_classes((permissions.AllowAny,))
# class ExternalSystemCrossReference(APIView):
#
#     class Meta(object):
#         abstract = True
#
#     def _read_and_action(self, request, func, pk):
#         '''
#         This method attempts to find an ExternalSystem object given the pk. If found it
#         submits it to func for processing. This function is expected to operate on the
#         response list object which is then returned by this function'''
#         es = None
#         try:
#             es = ExternalSystem.objects.get(pk=pk)
#         except ExternalSystem.DoesNotExist:
#             log.error("ExternalSystem[{0}] not found".format(pk))
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#         if es:
#             response = []
#             func(es, response)
#             # response = json.loads(json.dumps(response))
#             return Response (response)
#             # return json.dumps(response)
#
#     def getOrganization(self, org_id):
#         org = None
#         if org_id:
#             org = Organization.objects.get(pk=org_id)
#         return org
#
#
# class ExternalSystemRecords(ExternalSystemCrossReference):
#
#     def get(self, request, pk, **kwargs):
#         '''
#         This resource provides a response with all of the external records that are
#         associated with this external system. If the org_pk is provided,
#         then only external records whos subject record belong to the organization
#         will be returned. If the path is provide only external records with the
#         path will be included
#         '''
#
#         try:
#             org = self.getOrganization(kwargs.pop('org_pk', None))
#         except Organization.DoesNotExist:
#             log.error("Unable to retrieve ExternalSystemRecords. Organization not found")
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#         def process(es, response):
#             qs = ExternalRecord.objects.filter(external_system=es)
#
#             if org:
#                 qs = qs.filter(subject__organization=org)
#
#             for er in qs:
#                 r = er.responseFieldDict()
#                 response.append(r)
#
#         return self._read_and_action(request, process, pk)
#
#
# class ExternalSystemSubjects(ExternalSystemCrossReference):
#
#     def get(self, request, pk, **kwargs):
#         '''
#         This resource provides a response with all of the subjects that have
#         records associated with this external system. If the org_pk is provided,
#         then only subject records that belong to this organization will be returned
#         '''
#         try:
#             org = self.getOrganization(kwargs.pop('org_pk', None))
#         except Organization.DoesNotExist:
#             log.error("Unable to retrieve ExternalSystemSubjects. Organization not found")
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#         def process(es, response):
#             if not org:
#                 qs = es.subjects.all().distinct()
#             else:
#                 qs = es.subjects.filter(organization=org).distinct()
#             for s in qs:
#                 r = s.responseFieldDict()
#                 response.append(r)
#
#         return self._read_and_action(request, process, pk)
#
#
# @permission_classes((permissions.AllowAny,))
# class ExternalSystemQuery(APIView):
#
#     supported_accept_types = ['application/json']
#     model = 'core.models.identities.ExternalSystem'
#
#     def post(self, request):
#         """This method is intended querying for ExternalSystem records by name"""
#         content_type = request.META.get("CONTENT_TYPE")
#         response = []
#
#         if content_type == "application/json":
#
#             for s in request.data:
#                 nameval = s.get('name')
#                 urlval = s.get('url')
#
#                 if nameval:
#                     try:
#                         es = ExternalSystem.objects.get(name=nameval)
#                         response.append(
#                             {
#                                 "name": nameval,
#                                 "externalSystem":
#                                 es.responseFieldDict()
#                             }
#                         )
#                     except ExternalSystem.DoesNotExist:
#                         log.error("Unable to query for ExternalSystem no record found")
#                         response.append(
#                             {
#                                 "name": nameval,
#                                 "errors": [
#                                     {
#                                         "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
#                                     }
#                                 ]
#                             }
#                         )
#                 elif urlval:
#                     try:
#                         es = ExternalSystem.objects.get(url=urlval)
#                         response.append(
#                             {
#                                 "url": urlval,
#                                 "externalSystem": es.responseFieldDict()
#                             }
#                         )
#                     except ExternalSystem.DoesNotExist:
#                         log.error("Unable to query for ExternalSystem no record found")
#                         response.append(
#                             {
#                                 "url": urlval,
#                                 "errors": [
#                                     {
#                                         "Query": ErrorConstants.ERROR_NO_RECORD_FOUND_FOR_QUERY
#                                     }
#                                 ]
#                             }
#                         )
#                 else:
#                     log.error("Unable to query for ExternalSystem. Invalid query")
#                     response.append(
#                         {
#                             "errors": [
#                                 {
#                                     "Query": ErrorConstants.ERROR_INVALID_QUERY
#                                 }
#                             ]
#                         }
#                     )
#
#             # response = json.loads(json.dumps(response))
#             return Response(response)
#             # return json.dumps(response)
#
#
# @permission_classes((permissions.AllowAny,))
# class ExternalSystemResource(APIView):
#
#     supported_accept_types = ['application/json']
#     model = 'core.models.identities.ExternalSystem'
#
#     def get(self, request, pk):
#         es = None
#
#         try:
#             es = ExternalSystem.objects.get(pk=pk)
#         except ExternalSystem.DoesNotExist:
#             log.error("ExternalSystem[{0}] not found".format(pk))
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#         r = es.responseFieldDict()
#         #
#         # return json.dumps(r)
#         r = json.loads(json.dumps(r))
#         # serializer = ExternalSystemSerializer(es)
#         return Response(r)
#
#     def post(self, request):
#         """This method is intended for adding new ExternalSystem records"""
#
#         response = []
#
#         for s in request.data:
#             name = s.get('name')
#             form = ExternalSystemForm(s)
#             args = {'name': name}
#
#             FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)
#
#         print ("this is the response")
#         print (response)
#         return Response(response)
#         # return json.dumps(response)
#
#     def put(self, request):
#         """This method is intended for updating an existing ExternalSystem record"""
#
#         response = []
#
#         for item in request.data:
#             pkval = item.get('id')
#             s = item.get('external_system')
#
#             if not pkval or not s:
#                 log.error("Unable to update ExternalSystem. Identifier not provided")
#                 return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#             try:
#                 es = ExternalSystem.objects.get(pk=pkval)
#                 name = s.get('name', es.name)
#                 desc = s.get('description', es.description)
#                 url = s.get('url', es.url)
#                 js = {"name": name, "description": desc, "url": url}
#                 form = ExternalSystemForm(js, instance=es)
#                 FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})
#             except ExternalSystem.DoesNotExist:
#                 log.error("Unable to update ExternalSystem. ExternalSystem[{0}] not found".format(pkval))
#                 response.append(
#                     {
#                         'id': pkval,
#                         'success': False,
#                         'errors': [
#                             {
#                                 'id': ErrorConstants.ERROR_RECORD_ID_NOT_FOUND
#                             }
#                         ]
#                     }
#                 )
#         return Response (response)
#         # return json.dumps(response)
#
#     def delete(self, request, pk):
#         try:
#             es = ExternalSystem.objects.get(pk=pk)
#             es.delete()
#             return HttpResponse(status=status.HTTP_200_OK)
#         except ExternalSystem.DoesNotExist:
#             log.error("Unable to delete ExternalSystem. ExternalSystem[{0}] no found".format(pk))
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
