import json

# from restlib2.resources import Resource
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions
# from api.serializers import OrganizationSerializer

from core.models.identities import Relation, PedigreeSubjectRelation
from core.forms import PedigreeSubjectRelationForm
from api.helpers import FormHelpers


@permission_classes((permissions.AllowAny,))
class RelationResource(APIView):
    supported_accept_types = ['application/json']
    model = 'core.models.identities.Relation'

    def get(self, request, **kwargs):
        relations = Relation.objects.all()
        d = []
        for relation in relations:
            d.append(relation.to_dict())

        return Response(d)
        # return (json.dumps(d))


@permission_classes((permissions.AllowAny,))
class PedigreeSubjectRelationResource(APIView):
    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.PedigreeSubjectRelation'

    def output_relationships(self, relationship, relationships_dict):
        relationships_dict.append({
            "subject_org_id": relationship.subject_1.organization_subject_id,
            "subject_org": relationship.subject_1.organization.name,
            "subject_id": relationship.subject_1.id,
            "role": relationship.subject_1_role.desc,
            "related_subject_org_id": relationship.subject_2.organization_subject_id,
            "related_subject_org": relationship.subject_2.organization.name,
            "related_subject_id": relationship.subject_2.id
        })
        relationships_dict.append({
            "subject_org_id": relationship.subject_2.organization_subject_id,
            "subject_org": relationship.subject_2.organization.name,
            "subject_id": relationship.subject_2.id,
            "role": relationship.subject_2_role.desc,
            "related_subject_org_id": relationship.subject_1.organization_subject_id,
            "related_subject_org": relationship.subject_1.organization.name,
            "related_subject_id": relationship.subject_1.id
        })

    def relationships_by_protocol(self, protocol_id):
        relationships = []
        all_protocol_relationships = PedigreeSubjectRelation.objects.filter(protocol_id=protocol_id)
        for relationship in all_protocol_relationships:
            self.output_relationships(relationship, relationships)

    def relationships_by_subject(self, subject_id):
        relationships = []
        relationships_subs1 = PedigreeSubjectRelation.objects.filter(
                                subject_1=subject_id)
        # if given subject is 'subject 1' get subject1 role and subject 2
        for relationship in relationships_subs1:
            self.output_relationships(relationship, relationships)

        # if given subject is 'subject 2' get subject2 role and subject 1
        relationships_subs2 = PedigreeSubjectRelation.objects.filter(
                                subject_2=subject_id)
        for relationship in relationships_subs2:
            self.output_relationships(relationship, relationships)

        return relationships

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
        if subject_id:
            relationships = self.relationships_by_subject(subject_id)

        return Response(relationships)
        # return relationships

    def put(self, request):
        """This method is intended for updating an existing protocol relationship"""
        pass

    def post(self, request):
        """This method is intended for adding new Protocol Relationships"""
        content_type = request.META.get("CONTENT_TYPE")
        response = []

        if content_type == "application/json":

            for relationship in request.data:
                form = PedigreeSubjectRelationForm(relationship)
                args = {
                    'subject_1': relationship.get('subject_1'),
                    'subject_2': relationship.get('subject_2'),
                    'subject_1_role': relationship.get('subject_1_role'),
                    'subject_2_role': relationship.get('subject_2_role'),
                    'protocol_id': relationship.get('protocol_id')
                }
                FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)
            return Response(response)
            # return json.dumps(response)
