import json
from django.http import HttpResponse
from restlib2.resources import Resource
from django.db.models import Q

from core.models.identities import Relation, PedigreeSubjectRelation
from core.forms import PedigreeSubjectRelationForm
from api.helpers import FormHelpers



class RelationResource(Resource):
    supported_accept_types = ['application/json']
    model = 'core.models.identities.Relation'

    def get(self, request, **kwargs):
        relations = Relation.objects.all()
        d = []
        for relation in relations:
            d.append(relation.to_dict())

        return (json.dumps(d))


class PedigreeSubjectRelationResource(Resource):
    supported_accept_types = ['application/json', 'application/xml']
    model = 'core.models.identities.PedigreeSubjectRelation'

    def relationships_by_protocol(self, protocol_id):
        return PedigreeSubjectRelation.objects.filter(protocol_id=protocol_id)

    def relationships_by_subject(self, subject_id):
        relationships = []
        # relationships_subs = PedigreeSubjectRelation.objects.filter(
        #                         Q(subject_1=subject_id) |
        #                         Q(subject_2=subject_id))
        relationships_subs1 = PedigreeSubjectRelation.objects.filter(
                                subject_1=subject_id)
        # if given subject is 'subject 1' get subject1 role and subject 2
        for relationship in relationships_subs1:
            relationships.append({
                "subject_1_org_id": relationship.subject_1.organization_subject_id,
                "subject_1_org": relationship.subject_1.organization.name.responseFieldDict(),
                "role": relationship.subject_1_role.desc,
                "subject_2_org_id": relationship.subject_2.organization_subject_id,
                "subject_2_org": relationship.subject_2.organization.responseFieldDict()
            })
        # if given subject is 'subject 2' get subject2 role and subject 1
        relationships_subs2 = PedigreeSubjectRelation.objects.filter(
                                subject_2=subject_id)
        for relationship in relationships_subs2:
            relationships.append({
                "subject_1_org_id": relationship.subject_2.organization_subject_id,
                "subject_1_org": relationship.subject_2.organization.responseFieldDict(),
                "role": relationship.subject_2_role.desc,
                "subject_2_org_id": relationship.subject_1.organization_subject_id,
                "subject_2_org": relationship.subject_1.organization.responseFieldDict()
            })
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

        # relationship_dictionary = self.append_query_to_dict(relationships)
        # relationship_dictionary = (relationships)
        # return (json.dumps(relationship_dictionary))
        return relationships

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
            return json.dumps(response)
