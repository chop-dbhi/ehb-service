import json
from django.http import HttpResponse
from restlib2.resources import Resource

from core.models.identities import Relation


class RelationResource(Resource):
    supported_accept_types = ['application/json']
    model = 'core.models.identities.Relation'

    def get(self, request, **kwargs):
        relations = Relation.objects.all()
        d = []
        for relation in relations:
            d.append(relation.to_dict())

        return (json.dumps(d))
