import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from core.models.identities import Relation, SubjectFamRelation
from core.forms import SubjectFamRelationForm
from api.helpers import FormHelpers

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
        all_protocol_relationships = SubjectFamRelation.objects.filter(protocol_id=protocol_id)
        return(self.output_relationships(all_protocol_relationships))

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
        # get list of relationships based on protocol id
        if protocol_id:
            relationships = self.relationships_by_protocol(protocol_id)
        # get list of relationships based on subject id
        elif subject_id:
            relationships = self.relationships_by_subject(subject_id)
        # get familial relationship types
        else:
            relationships = self.output_relationship_types()

        return Response(relationships)

    def put(self, request):
        """This method is intended for updating an existing protocol relationship"""
        pass

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
