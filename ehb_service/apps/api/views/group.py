from django.http import HttpResponse
import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import permissions

from core.models.identities import Group, SubjectGroup, Subject, ExternalRecord, ExternalRecordGroup
from core.forms import GroupForm
from api.helpers import FormHelpers
from constants import ErrorConstants

log = logging.getLogger(__name__)


@permission_classes((permissions.AllowAny,))
class ClientKeyResource(APIView):
    # def decode_key(self, key, request):
    #     enc_key = request.META.get(key)
    #     if enc_key:
    #         try:
    #             return base64.b64decode(enc_key)
    #         except Exception:
    #             return None

    def client_key(self, request):
        return request.META.get('HTTP_GROUP_CLIENT_KEY')
    #        return self.decode_key('HTTP_GROUP_CLIENT_KEY', request)


class XGroupResource(ClientKeyResource):
    mimetypes = ('application/json', 'application/xml')

    def XModel(self):
        pass

    def XModelLabel(self):
        pass

    def XGroupModel(self):
        pass

    def XGroupItems(self, xgroup):
        pass

    class Meta(object):
        abstract = True

    def get(self, request, pk):

        XGroup = self.XGroupModel()

        try:
            grp = Group.objects.get(pk=pk)

            # First need to check that if this group is locked also check client_key
            if grp.is_locking and not grp.verify_client_key(self.client_key(request)):
                log.error("Cannot verify client key on a locked group")
                return Response(status=status.HTTP_403_FORBIDDEN)

            try:
                response = []
                X_grp = XGroup.objects.get(group=grp)
                for x in self.XGroupItems(X_grp).all():
                    response.append(x.responseFieldDict())
                return Response(response)
                # return json.dumps(response)
            except XGroup.DoesNotExist:
                log.error("No records found for group [{0}].".format(pk))
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            log.error("Group [{0}] does not exist.".format(pk))
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        response = []

        try:
            grp = Group.objects.get(pk=pk)

            # First need to check that if this group is locked. If it is also check client_key
            if grp.is_locking and not grp.verify_client_key(self.client_key(request)):
                log.error("Group query made with incorrect client key or the group is locked")
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Find the corresponding subject group, create if needed
            XGroup = self.XGroupModel()
            X_grp = None

            try:
                X_grp = XGroup.objects.get(group=grp)
            except XGroup.DoesNotExist:
                log.warning("Sub group {0} does not exist so its being created.".format(grp))
                X_grp = XGroup(group=grp)
                X_grp.save()

            # Add each X in the request data to the group if the X exists
            X = self.XModel()

            for x_id in request.data:
                try:
                    x = X.objects.get(pk=x_id)
                    self.XGroupItems(X_grp).add(x)
                    response.append({'id': x_id, 'success': True})
                except X.DoesNotExist:
                    log.error("Unable to add {0} to the group as it x_id:{0} does not exist".format(x_id))
                    response.append({'id': x_id, 'success': False, 'errors': ErrorConstants.ERROR_ID_NOT_FOUND})

            return Response(response)

        except Group.DoesNotExist:
            log.error("Group {0} does not exist".format(pk))
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, grp_pk, x_pk):
        try:
            grp = Group.objects.get(pk=grp_pk)

            # First need to check that if this group is locked. If it is also check client_key
            if grp.is_locking and not grp.verify_client_key(self.client_key(request)):
                log.error("Group query made with incorrect client key or the group is locked")
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Find the corresponding subject group
            XGroup = self.XGroupModel()
            X_grp = None

            try:
                X_grp = XGroup.objects.get(group=grp)
            except XGroup.DoesNotExist:
                log.error("Sub group {0} does not exist.".format(grp))
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Remove subject from Group
            X = self.XModel()

            try:
                x = X.objects.get(pk=x_pk)
                self.XGroupItems(X_grp).remove(x)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except X.DoesNotExist:
                log.error('Unable to delete record from group. Record does not exist')
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            log.error("Group {0} does not exist.".format(grp_pk))
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, **kwargs):
        '''PUTS are not supported, should use POST'''
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SubjectGroupResource(XGroupResource):
    def XModel(self):
        return Subject

    def XModelLabel(self):
        return 'subject'

    def XGroupModel(self):
        return SubjectGroup

    def XGroupItems(self, xgroup):
        return xgroup.subjects


class RecordGroupResource(XGroupResource):
    def XModel(self):
        return ExternalRecord

    def XModelLabel(self):
        return 'external_record'

    def XGroupModel(self):
        return ExternalRecordGroup

    def XGroupItems(self, xgroup):
        return xgroup.external_records


class GroupResource(ClientKeyResource):

    def get(self, request):
        dict_ = request.GET
        key = 'id'
        val = dict_.get(key)

        if not val:
            key = 'name'
            val = dict_.get(key)

        if val:
            group = None
            try:

                if not Group.objects.all():
                    log.error('Unable to retrieve Groups from configured database')
                    return Response(status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

                if key == 'id':
                    group = Group.objects.filter(pk=val)
                else:
                    group = Group.objects.filter(name=val)

                if group.__len__() == 1:
                    g = group[0]
                    rd = g.responseFieldDict()
                    # For security reasons we do not want to give the client key to GET requests
                    rd.pop('client_key')
                    rd.pop('ehb_key_id')
                    rd['ehb_key'] = g.ehb_key.key
                    return Response(rd)
                else:
                    log.error('Unable to find group with provided criteria')
                    return Response(status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        '''This method is intended for creating Groups.'''
        response = []

        for g in request.data:
            form = GroupForm(g)
            args = {'name': g.get('name')}
            rd = FormHelpers.processFormJsonResponse(form, response, valid_dict=args, invalid_dict=args)

            if rd.get('success', False):
                grp = Group.objects.get(pk=rd.get('id'))
                rd['ehb_key'] = grp.ehb_key.key

        return Response(response)

    def put(self, request):
        '''This method is intended for updating Groups.'''
        response = []

        for item in request.data:
            pkval = item.get('id')
            g = item.get('group')

            if not (pkval and g):
                log.error("Unable to update group. No group or ID provided")
                return Response(status=status.HTTP_400_BAD_REQUEST)

            current_client_key = g.get('current_client_key', None)

            if not current_client_key:
                log.error("Unable to update group. No client key provided")
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                grp = Group.objects.get(pk=pkval)

                if not grp.verify_client_key(current_client_key):
                    log.error("Unable to update group. Bad client key")
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

                name = g.get('name', grp.name)
                lock = g.get('is_locking', grp.is_locking)
                des = g.get('description', grp.description)
                client_key = g.get('client_key', current_client_key)
                js = {"name": name, "client_key": client_key, "is_locking": lock, "description": des}
                form = GroupForm(js, instance=grp)
                rd = FormHelpers.processFormJsonResponse(form, response, invalid_dict={'id': pkval})

                if rd.get('success', False):
                    grp = Group.objects.get(pk=rd.get('id'))
                    rd['ehb_key'] = grp.ehb_key.key
                else:
                    return Response
            except Group.DoesNotExist:
                log.error("Unable to update group. Group does not exist.")
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

    def delete(self, request):
        ck = self.client_key(request)

        if not ck:
            log.error("Unable to delete group. Client key not provided")
            return Response(status=status.HTTP_403_FORBIDDEN)

        qs = request.META.get('QUERY_STRING')

        if qs:
            d = {}
            try:
                qs = qs.strip()

                for item in qs.split('&'):
                    k, v = item.split('=')
                    d[k] = v

                grp = None
                gid = d.get('id')

                if gid:
                    grp = Group.objects.get(pk=gid)
                else:
                    name = d.get('name')
                    if name:
                        grp = Group.objects.get(name=name)

                if not grp.verify_client_key(ck):
                    log.error("Unable to delete group. Bad client key")
                    return Response(status=status.HTTP_403_FORBIDDEN)
                grp.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            except Group.DoesNotExist:
                log.error("Unable to delete group. Group not found")
                return Response(status=status.HTTP_404_NOT_FOUND)

        log.error("Unable to delete group. No query string provided")
        return Response(status=status.HTTP_400_BAD_REQUEST)
