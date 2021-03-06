import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from .constants import ErrorConstants

from core.models.identities import Relation, SubjectFamRelation
from core.forms import SubjectFamRelationForm
from api.helpers import FormHelpers
log = logging.getLogger(__name__)

class LinkRelationView(APIView):

    def get(self, request, **kwargs):
        relations = Relation.objects.all()
        d = []
        for relation in relations:
            d.append(relation.to_dict())

        return Response(d)


class SubjectFamRelationView(APIView):
    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.SubjectFamRelation'


    def output_relationship_types(self):
        return self.append_query_to_dict(Relation.objects.filter(typ__istartswith='familial'))

    def output_relationships(self, relationship_objects, relationships_dict=[]):
        for rel in relationship_objects:
            relationships_dict.append(rel.to_dict())
        return relationships_dict

    def relationships_by_protocol(self, protocol_id):
        relationships_dict = []
        all_protocol_relationships = list(SubjectFamRelation.objects.filter(protocol_id=protocol_id))
        for relationship in all_protocol_relationships:
            print(relationship.subject_1.id)
            relationships_dict.append({
                "subject_1_id": relationship.subject_1.id,
                "subject_1_org_id": relationship.subject_1.organization_subject_id,
                "subject_2_id": relationship.subject_2.id,
                "subject_2_org_id": relationship.subject_2.organization_subject_id,
                "subject_1_role": relationship.subject_1_role.desc,
                "subject_2_role": relationship.subject_2_role.desc,
                "protocol_id": relationship.protocol_id,
                "id": relationship.id
            })
        return(relationships_dict)

    def relationships_by_subject(self, subject_id):
        relationships_dict = []

        subject_1_rel_obj = SubjectFamRelation.objects.filter(
                                subject_1=subject_id)
        self.output_relationships(subject_1_rel_obj, relationships_dict)

        subject_2_rel_obj = SubjectFamRelation.objects.filter(
                                subject_2=subject_id)
        self.output_relationships(subject_2_rel_obj, relationships_dict)
        return relationships_dict

    def append_query_to_dict(self, query):
        dict = []
        for item in query:
            dict.append(item.to_dict())
        return dict

    def get(self, request, **kwargs):
        protocol_id = kwargs.pop("protocol_id", None)
        subject_id = kwargs.pop("subject_id", None)
        relationship_id = kwargs.pop("relationship_id", None)
        # get list of relationships based on protocol id
        if protocol_id:
            relationships = self.relationships_by_protocol(protocol_id)
        # get list of relationships based on subject id
        elif subject_id:
            relationships = self.relationships_by_subject(subject_id)
        # return all elements of a single relationship
        elif relationship_id:
            try:
                relationships = SubjectFamRelation.objects.filter(id=relationship_id)[0].to_dict()
            except:
                response = {
                        'id': relationship_id,
                        'success': False,
                        'errors': [
                            {
                                'id': ErrorConstants.ERROR_SUBJ_FAM_RELATIONSHIP_NOT_FOUND
                            }
                        ]
                    }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        # get familial relationship types
        else:
            relationships = self.output_relationship_types()

        return Response(relationships)

    def put(self, request):
        """This method is intended for updating an existing protocol relationship
        This API request will take in ID and subject relationship attributes

             "id": "x",              PK of subject relationship
             "subject_1": 6738,      PK of subject
             "subject_2": 6739,      PK of subject
             "subject_1_role": 14,   PK of subject role
             "subject_2_role": 15,   PK of subject role
             "protocol_id": 1        PK of protocol in the BRP
        """
        response = []

        for item in request.data:
            pkval = item.get('id')
            subj_relation = SubjectFamRelation.objects.get(pk=pkval)

            if not pkval:
                log.error("Unable to update Subject relationship. No identifier provided")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                args = {
                    "subject_1": item.get('subject_1'),
                    "subject_2": item.get('subject_2'),
                    "subject_1_role": item.get('subject_1_role'),
                    "subject_2_role": item.get('subject_2_role'),
                    "protocol_id": item.get('protocol_id', subj_relation.protocol_id)
                }
                form = SubjectFamRelationForm(args, instance=subj_relation)
                FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})
            except SubjectFamRelation.DoesNotExist:
                log.error("Unable to update Subject relationship. Subject relationship[{0}] does not exist".format(pkval))
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

    def post(self, request):
        """This method is intended for adding new Protocol Relationships"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for relationship in request.data:
                form = SubjectFamRelationForm(relationship)
                args = {
                    'subject_1': relationship.get('subject_1'),
                    'subject_2': relationship.get('subject_2'),
                    'subject_1_role': relationship.get('subject_1_role'),
                    'subject_2_role': relationship.get('subject_2_role'),
                    'protocol_id': relationship.get('protocol_id')
                }
                FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)
            return Response(response)

    def delete(self, request, relationship_id):
        """This method is intended for deleting new Protocol Relationships"""
        response = []

        try:
            subj_relation = SubjectFamRelation.objects.get(pk=relationship_id)
            subj_relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SubjectFamRelation.DoesNotExist:
            response.append(
                {
                    'id': relationship_id,
                    'success': False,
                    'errors': [
                        {
                            'id': ErrorConstants.ERROR_RECORD_ID_NOT_FOUND
                        }
                     ]
                }
            )
            log.error("Unable to update Subject relationship. Subject relationship[{0}] does not exist".format(relationship_pk))

            return Response(response, status=status.HTTP_404_NOT_FOUND)
