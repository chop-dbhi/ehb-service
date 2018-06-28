import json
from django.http import HttpResponse
from restlib2.resources import Resource

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
    supported_accept_types = ['application/json']
    model = 'core.models.identities.PedigreeSubjectRelation'

    def get(self, request, protocol):
        relationships = PedigreeSubjectRelation.objects.get(protocol=protocol)
        d = []
        for relationship in relationships:
            d.append(relationships.to_dict())

        return (json.dumps(d))

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
