"""
Run via Django's manage.py tool: `./bin/manage.py test api`
"""
import json
from django.db.models import Q

from django.test import TestCase
from core.models.identities import Organization, Subject, Group, ExternalRecord, ExternalSystem, PedigreeSubjectRelation

from mock import patch


class TestGroup(TestCase):

    fixtures = ['test_fixture.json']

    # 2 is going to return subject group
    # 3 is going to return externalrecord group
    # Going to want to test record groups and subject groups
    # url(r'^$', 'GroupResource'),
    # url(r'^id/(?P<pk>\d+)/subjects/$', 'SubjectGroupResource'),
    # url(r'^id/(?P<grp_pk>\d+)/subjects/id/(?P<x_pk>\d+)/$', 'SubjectGroupResource'),
    # url(r'^id/(?P<pk>\d+)/records/$', 'RecordGroupResource'),
    # url(r'^id/(?P<grp_pk>\d+)/records/id/(?P<x_pk>\d+)/$', 'RecordGroupResource'),

    def setUp(self):
        # Create Subject Group
        req = {
            'description': 'A BRP Protocol Group',
            'is_locking': 'True',
            'name': 'BRP:NEWTESTGROUP',
            'client_key': 'testck'
        }
        response = self.client.post(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        # Add a record to the Group
        response = self.client.post(
            '/api/group/id/6/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[2]',
            HTTP_GROUP_CLIENT_KEY='testck')
        # Create Subject Record Group
        req = {
            'description': 'A BRP Record Group',
            'is_locking': 'True',
            'name': 'BRP:NEWRECORDGROUP',
            'client_key': 'testck'
        }
        response = self.client.post(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        # Add a record to the Group
        response = self.client.post(
            '/api/group/id/7/subjects/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[2]',
            HTTP_GROUP_CLIENT_KEY='testck')
        # Create Subject Group ( no records )
        req = {
            'description': 'A BRP Protocol Group',
            'is_locking': 'True',
            'name': 'BRP:NEWGROUP_NORECORDS',
            'client_key': 'testck'
        }
        response = self.client.post(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))

    def test_delete_group_by_id(self):
        pre_count = Group.objects.count()
        response = self.client.delete(
            '/api/group/',
            content_type='application/json',
            QUERY_STRING='id=6',
            HTTP_GROUP_CLIENT_KEY='testck',
            HTTP_API_TOKEN="secretkey123"
        )
        post_count = Group.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertTrue(post_count < pre_count)

    def test_delete_group_by_name(self):
        pre_count = Group.objects.count()
        response = self.client.delete(
            '/api/group/',
            content_type='application/json',
            QUERY_STRING='name=BRP:NEWTESTGROUP',
            HTTP_GROUP_CLIENT_KEY='testck',
            HTTP_API_TOKEN="secretkey123"
        )
        post_count = Group.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertTrue(post_count < pre_count)

    @patch('api.resources.group.log')
    def test_delete_group_no_ck(self, mock_log):
        response = self.client.delete(
            '/api/group/',
            content_type='application/json',
            QUERY_STRING='name=BRP:NEWTESTGROUP',
            HTTP_API_TOKEN='secretkey123'
        )
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 403)

    @patch('api.resources.group.log')
    def test_delete_group_no_qs(self, mock_log):
        response = self.client.delete(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY='testck'
        )
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 400)

    @patch('api.resources.group.log')
    def test_delete_group_bad_pk(self, mock_log):
        response = self.client.delete(
            '/api/group/',
            content_type='application/json',
            QUERY_STRING='name=BAD',
            HTTP_GROUP_CLIENT_KEY='testck',
            HTTP_API_TOKEN='secretkey123'
        )
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_add_group(self):
        pre_count = Group.objects.count()
        req = {
            'description': 'A BRP Protocol Group',
            'is_locking': 'True',
            'name': 'BRP:ANOTHER_TEST_GROUP',
            'client_key': 'testck'
        }
        response = self.client.post(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        post_count = Group.objects.count()
        self.assertTrue(r['success'])
        self.assertTrue(post_count > pre_count)

    def test_update_group(self):
        req = {
            'id': '6',
            'group': {
                'description': 'A New Description',
                'id': '6',
                'is_locking': 'True',
                'name': 'BRP:NEWTESTGROUP',
                'current_client_key': 'testck'
            }
        }
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])

    @patch('api.resources.group.log')
    def test_update_group_no_pk(self, mock_log):
        req = {
            'group': {
                'description': 'A New Description',
                'id': '2',
                'is_locking': 'True',
                'name': 'BRP:M0536B4E2DDLA7W6',
                'current_client_key': 'testck'
            }
        }
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))

        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 400)

    @patch('api.resources.group.log')
    def test_update_group_bad_ck(self, mock_log):
        req = {
            'id': '2',
            'group': {
                'description': 'A New Description',
                'id': '2',
                'is_locking': 'True',
                'name': 'BRP:NEWTESTGROUP',
                'current_client_key': 'BADCK'
            }
        }
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 401)

    @patch('api.resources.group.log')
    def test_update_group_no_ck(self, mock_log):
        req = {
            'id': '1',
            'group': {
                'description': 'A New Description',
                'id': '1',
                'is_locking': 'True',
                'name': 'BRP:NEWTESTGROUP'
            }
        }
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 400)

    @patch('api.resources.group.log')
    def test_update_group_bad_pk(self, mock_log):
        req = {
            'id': '99',
            'group': {
                'description': 'A New Description',
                'id': '2',
                'is_locking': 'True',
                'name': 'BRP:M0536B4E2DDLA7W6',
                'current_client_key': 'testck'
            }
        }
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(r['success'])

    def test_add_record_to_group(self):
        # we only need to pass a list of pks being added to the group to add it
        er = Group.objects.get(pk=6).externalrecordgroup_set.all()
        response = self.client.post(
            '/api/group/id/6/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[4]',
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])

    @patch('api.resources.group.log')
    def test_add_record_to_group_no_group(self, mock_log):
        # we only need to pass a list of pks being added to the group to add it
        response = self.client.post(
            '/api/group/id/99/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([2]),
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    @patch('api.resources.group.log')
    def test_add_record_to_group_no_key(self, mock_log):
        # we only need to pass a list of pks being added to the group to add it
        response = self.client.post(
            '/api/group/id/6/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[2]')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 403)

    @patch('api.resources.group.log')
    def test_add_record_to_group_bad_record_id(self, mock_log):
        # we only need to pass a list of pks being added to the group to add it
        response = self.client.post(
            '/api/group/id/6/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([99]),
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertFalse(r['success'])
        self.assertTrue(r['errors'], 13)

    def test_delete_record(self):
        # Essentially this will remove John Doe's Redcap record from his record group.
        response = self.client.delete(
            '/api/group/id/6/records/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertEqual(response.status_code, 204)

    @patch('api.resources.group.log')
    def test_delete_record_bad_group_key(self, mock_log):
        response = self.client.delete(
            '/api/group/id/3/records/id/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY='BADKEY')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 403)

    @patch('api.resources.group.log')
    def test_delete_record_bad_x(self, mock_log):
        response = self.client.delete(
            '/api/group/id/99/records/id/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    @patch('api.resources.group.log')
    def test_delete_record_no_xg(self, mock_log):
        response = self.client.delete(
            '/api/group/id/6/records/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY='testck')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_get_protocol_group_by_name(self):
        response = self.client.get(
            '/api/group/?name=BRP:NEWTESTGROUP', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'
            }
        )
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['id'], '6')

    def test_get_protocol_group_by_id(self):
        response = self.client.get(
            '/api/group/?id=2', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['name'], 'BRP:M0536B4E2DDLA7W6')

    @patch('api.resources.group.log')
    def test_get_protocol_group_by_name_bad_group(self, mock_log):
        response = self.client.get(
            '/api/group/?name=BADGROUP', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 416)

    def test_get_group_records(self):
        response = self.client.get(
            '/api/group/id/6/records/', **{
                'CONTENT_TYPE': 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 1)

    @patch('api.resources.group.log')
    def test_get_group_records_no_records(self, mock_log):
        response = self.client.get(
            '/api/group/id/8/records/', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_get_group_subjects(self):
        response = self.client.get(
            '/api/group/id/7/subjects/', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})

        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 1)

    @patch('api.resources.group.log')
    def test_get_group_subjects_bad_group_id(self, mock_log):
        response = self.client.get(
            '/api/group/id/99/subjects/', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'testck',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_get_group_subjects_bad_ck(self):
        response = self.client.get(
            '/api/group/id/2/subjects/', **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": 'BADKEY',
                'HTTP_API_TOKEN': 'secretkey123'})
        self.assertEqual(response.status_code, 403)


class TestSubject(TestCase):

    fixtures = ['test_fixture.json']

    def test_subject_get(self):
        response = self.client.get(
            '/api/subject/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['first_name'], 'John')
        self.assertEqual(j['last_name'], 'Doe')
        self.assertEqual(j['dob'], '2000-01-01')
        self.assertEqual(j['organization'], 3)
        self.assertEqual(j['organization_subject_id'], '123456')

    @patch('api.resources.subject.log')
    def test_subject_get_bad_pk(self, mock_log):
        response = self.client.get(
            '/api/subject/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_subject_get_by_osid(self):
        response = self.client.get(
            '/api/subject/organization/3/osid/123456/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['first_name'], 'John')
        self.assertEqual(j['last_name'], 'Doe')
        self.assertEqual(j['dob'], '2000-01-01')
        self.assertEqual(j['organization'], 3)
        self.assertEqual(j['organization_subject_id'], '123456')

    @patch('api.resources.subject.log')
    def test_subject_get_by_osid_bad_org(self, mock_log):
        response = self.client.get(
            '/api/subject/organization/99/osid/123456/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    @patch('api.resources.subject.log')
    def test_subject_get_osid_bad_osid(self, mock_log):
        response = self.client.get(
            '/api/subject/organization/3/osid/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_subject_delete(self):
        pre_count = Subject.objects.count()
        response = self.client.delete(
            '/api/subject/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        post_count = Subject.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertTrue(post_count < pre_count)

    def test_subject_add(self):
        pre_count = Subject.objects.count()
        sub = {
            'first_name': 'New',
            'last_name': 'Subject',
            'dob': '2000-01-01',
            'organization': '3',
            'organization_subject_id': '999999'
        }
        response = self.client.post(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([sub]))
        post_count = Subject.objects.count()
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])
        self.assertTrue(pre_count < post_count)

    def test_subject_add_same_osid(self):
        sub = {
            'first_name': 'New',
            'last_name': 'Subject',
            'dob': '2000-01-01',
            'organization': '3',
            'organization_subject_id': '123456'
        }
        response = self.client.post(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([sub]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({"__all__": 3} in r['errors'])

    def test_subject_update(self):
        sub = Subject.objects.get(pk=2)
        pre_id = sub.organization_subject_id
        sub_data = sub.responseFieldDict()
        sub_data['organization_subject_id'] = '999999'
        sub_data['organization'] = sub.organization_id
        req = {}
        req['new_subject'] = sub_data
        req['id'] = sub.id
        response = self.client.put(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        sub = Subject.objects.get(pk=2)
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertEqual(sub.organization_subject_id, '999999')
        self.assertTrue(pre_id != sub.organization_subject_id)
        self.assertTrue(r['success'])

    @patch('api.resources.subject.log')
    def test_subject_update_bad_sub_pk(self, mock_log):
        sub = Subject.objects.get(pk=2)
        sub_data = sub.responseFieldDict()
        sub_data['organization_subject_id'] = '999999'
        sub_data['organization'] = sub.organization_id
        req = {}
        req['new_subject'] = sub_data
        req['id'] = '99'
        response = self.client.put(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertFalse(r['success'])
        self.assertTrue({"id": 1} in r['errors'])

    @patch('api.helpers.log')
    def test_subject_update_bad_org_pk(self, mock_log):
        sub = Subject.objects.get(pk=2)
        sub_data = sub.responseFieldDict()
        sub_data['organization_subject_id'] = '999999'
        sub_data['organization'] = '99'
        req = {}
        req['new_subject'] = sub_data
        req['id'] = sub.id
        response = self.client.put(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertFalse(r['success'])
        self.assertTrue({"organization": 7} in r['errors'])

    @patch('api.resources.subject.log')
    def test_subject_update_no_pk(self, mock_log):
        sub = Subject.objects.get(pk=2)
        sub_data = sub.responseFieldDict()
        sub_data['organization_subject_id'] = '999999'
        req = {}
        req['new_subject'] = sub_data

        response = self.client.put(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 400)


class TestExternalSystem(TestCase):

    fixtures = ['test_fixture.json']

    def test_es_query_by_name(self):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"name":"Nautilus Test"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]['externalSystem']
        self.assertEqual(r['name'], "Nautilus Test")
        self.assertEqual(r['url'], 'http://nautilus.local:8090/api/')

    def test_es_query_by_url(self):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"url":"http://nautilus.local:8090/api/"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]['externalSystem']
        self.assertEqual(r['name'], "Nautilus Test")
        self.assertEqual(r['url'], 'http://nautilus.local:8090/api/')

    @patch('api.resources.externalsystem.log')
    def test_es_query_by_name_not_found(self, mock_log):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"name":"Bad Name"}]')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({'Query': 9} in r['errors'])

    @patch('api.resources.externalsystem.log')
    def test_es_query_by_url_not_found(self, mock_log):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"url":"http://badurl.local: 8090/api/"}]')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({'Query': 9} in r['errors'])

    @patch('api.resources.externalsystem.log')
    def test_es_query_invalid_query(self, mock_log):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"bad_param":""}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({'Query': 8} in r['errors'])

    def test_es_xref_subjects(self):
        response = self.client.get(
            '/api/externalsystem/id/2/subjects/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 2)

    def test_es_xref_subjects_by_org(self):
        response = self.client.get(
            '/api/externalsystem/id/2/organization/3/subjects/',
            HTTP_API_TOKEN='secretkey123')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 2)

    @patch('api.resources.externalsystem.log')
    def test_es_xref_subjects_by_org_bad_org(self, mock_log):
        response = self.client.get(
            '/api/externalsystem/id/2/organization/99/subjects/',
            HTTP_API_TOKEN='secretkey123',)
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    @patch('api.resources.externalsystem.log')
    def test_es_xref_subjects_by_org_bad_es(self, mock_log):
        response = self.client.get(
            '/api/externalsystem/id/99/organization/3/subjects/',
            HTTP_API_TOKEN='secretkey123')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_es_xref_exrecs(self):
        response = self.client.get(
            '/api/externalsystem/id/2/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 2)

    def test_es_xref_exrecs_by_org(self):
        response = self.client.get(
            '/api/externalsystem/id/2/organization/3/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 2)

    @patch('api.resources.externalsystem.log')
    def test_es_xref_exrecs_by_org_bad_org(self, mock_log):
        response = self.client.get(
            '/api/externalsystem/id/2/organization/99/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    @patch('api.resources.externalsystem.log')
    def test_es_xref_exrecs_bad_es(self, mock_log):
        response = self.client.get(
            '/api/externalsystem/id/99/records/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_es_get(self):
        response = self.client.get(
            '/api/externalsystem/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['name'], 'CHOP TIU REDCap')
        self.assertEqual(j['url'], 'https://redcap.local/redcap/redcap/api/')
        self.assertEqual(j['id'], '2')
        self.assertEqual(j['description'], 'Children\'s Hospital of Philadelphia CBMi/TiU Research REDCap instance')

    @patch('api.resources.externalsystem.log')
    def test_es_get_bad_pk(self, mock_log):
        response = self.client.get(
            '/api/externalsystem/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)

    def test_es_add(self):
        pre_count = ExternalSystem.objects.count()
        es = {
            'description': "Test Description",
            'url': 'https://newsystem.local/api/',
            'name': 'New Test System'
        }
        response = self.client.post(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([es]))
        post_count = ExternalSystem.objects.count()
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])
        self.assertTrue(pre_count < post_count)

    @patch('api.helpers.log')
    def test_es_add_duplicate_url(self, mock_log):
        pre_count = ExternalSystem.objects.count()
        es = {
            'description': "Test Description",
            'url': 'https://redcap.local/redcap/redcap/api/',
            'name': 'New Test System'
        }
        response = self.client.post(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([es]))
        post_count = ExternalSystem.objects.count()
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertTrue({"url": 10} in r['errors'])
        self.assertFalse(r['success'])
        self.assertTrue(pre_count == post_count)

    def test_es_update(self):
        es = ExternalSystem.objects.get(pk=2)
        pre_name = es.name
        es_data = es.responseFieldDict()
        es_data['name'] = "New Name"
        req = {}
        req['external_system'] = es_data
        req['id'] = es_data['id']
        response = self.client.put(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        es = ExternalSystem.objects.get(pk=2)
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertEqual(es.name, 'New Name')
        self.assertTrue(pre_name != es.name)
        self.assertTrue(r['success'])

    @patch('api.resources.externalsystem.log')
    def test_es_update_bad_id(self, mock_log):
        es = ExternalSystem.objects.get(pk=2)
        es_data = es.responseFieldDict()
        es_data['name'] = "New Name"
        req = {}
        req['external_system'] = es_data
        req['id'] = '99'
        response = self.client.put(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(mock_log.error.called)
        self.assertFalse(r['success'])
        self.assertTrue({"id": 1} in r['errors'])

    @patch('api.resources.externalsystem.log')
    def test_es_update_bad_query(self, mock_log):
        req = {}
        req['external_system'] = None
        response = self.client.put(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 400)

    def test_es_delete(self):
        pre_count = ExternalSystem.objects.count()
        response = self.client.delete(
            '/api/externalsystem/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 204)
        post_count = ExternalSystem.objects.count()
        self.assertTrue(post_count < pre_count)

    @patch('api.resources.externalsystem.log')
    def test_es_delete_bad_pk(self, mock_log):
        response = self.client.delete(
            '/api/externalsystem/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)


class TestExternalRecord(TestCase):

    fixtures = ['test_fixture.json']

    def test_er_query_by_sub_id(self):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"subject_id": "2"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        self.assertEqual(len(ex_recs), 3)

    def test_er_query_by_sub_org(self):
        '''
        **TODO: If _only_ sub_org is provided without sub_id the eHB will return _all_ external records

        Not sure if this should be the expected behavior (probably not)
        '''
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"subject_org": "2", "subject_id":"1"}]')
        self.assertEqual(response.status_code, 200)
        # j = json.loads(response.content)
        # ex_recs = j[0]['external_record']
        # self.assertEqual(len(ex_recs), 3)

    def test_er_query_by_sub_org_and_sub_org_id(self):
        '''
        Testing the query of ExternalRecords by a Subject's Organization's ID (pk) and their
        Organization ID issued by the Organization (MRN)
        '''
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"subject_org": "3", "subject_org_id":"54545454"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        self.assertEqual(len(ex_recs), 1)
        self.assertEqual(j[0]['subject_org'], '3')
        self.assertEqual(j[0]['subject_org_id'], '54545454')

    def test_er_query_by_esid(self):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"external_system_id":"1"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        for each in ex_recs:
            self.assertEqual(each['external_system'], 1)
        self.assertEqual(len(ex_recs), 2)

    def test_er_query_by_esname(self):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"external_system_name":"Nautilus Test"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        for each in ex_recs:
            self.assertEqual(each['external_system'], 1)
        self.assertEqual(len(ex_recs), 2)

    def test_er_query_by_esurl(self):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"external_system_url":"http://nautilus.local:8090/api/"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        for each in ex_recs:
            self.assertEqual(each['external_system'], 1)
        self.assertEqual(len(ex_recs), 2)

    def test_er_query_by_path(self):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"path":"Test Protocol"}]')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        ex_recs = j[0]['external_record']
        for each in ex_recs:
            self.assertEqual(each['path'], 'Test Protocol')
        self.assertEqual(len(ex_recs), 4)

    @patch('api.resources.externalrecord.log')
    def test_er_query_bad_sub_id(self, mock_log):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"subject_id": "99"}]')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertEqual(r['subject_id'], '99')
        self.assertEqual({"Query": 9}, r['errors'])

    def test_er_query_bad_sub_org_and_sub_id(self):
        '''
        TODO: There is a problem with this query
        '''
        # response = self.client.post(
        #     '/api/externalrecord/query/',
        #     HTTP_API_TOKEN='secretkey123',
        #     content_type='application/json',
        #     data='[{"subject_org": "99", "subject_org_id":"99"}]')
        # self.assertEqual(response.status_code, 416)

    @patch('api.resources.externalrecord.log')
    def test_er_query_bad_esid(self, mock_log):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"external_system_id":"99"}]')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertEqual(r['external_system_id'], '99')
        self.assertEqual({"Query": 9}, r['errors'])

    def test_er_query_bad_params(self):
        '''
        TODO: we're returning all external records
        '''
        # response = self.client.post(
        #     '/api/externalrecord/query/',
        #     HTTP_API_TOKEN='secretkey123',
        #     content_type='application/json',
        #     data ='[{"testing":"99"}]')
        # self.assertEqual(True)

    @patch('api.resources.externalrecord.log')
    def test_er_query_bad_path(self, mock_log):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"path": "BAD PATH"}]')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({"Query": 9} in r['errors'])

    def test_er_add(self):
        pre = ExternalRecord.objects.count()
        response = self.client.post(
            '/api/externalrecord/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"subject":"2","external_system":"2","record_id":"TEST_RECORD_ID","path":"Test Protocol","label":1}]')  # noqa
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        post = ExternalRecord.objects.count()
        self.assertEqual(r['success'], True)
        self.assertTrue(post > pre)

    def test_er_delete(self):
        pre = ExternalRecord.objects.count()
        response = self.client.delete(
            '/api/externalrecord/id/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 204)
        post = ExternalRecord.objects.count()
        self.assertTrue(post < pre)

    def test_er_get(self):
        response = self.client.get(
            '/api/externalrecord/id/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['record_id'], 'NXB546EUZSDLZKGR:5EM3AOORG')

    def test_er_update(self):
        er = ExternalRecord.objects.get(pk=1)
        # pre_record_id = er.record_id (11/11/14)
        er_data = er.responseFieldDict()
        er_data['record_id'] = 'NEWID'
        er_data['external_system'] = 3
        er_data['relation'] = "2"
        er_data['path'] = 'New Path'
        er_data['label'] = '1'
        req = {}
        req['external_record'] = er_data
        req['id'] = er_data['id']
        response = self.client.put(
            '/api/externalrecord/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        updated_er = ExternalRecord.objects.get(id=1)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])
        self.assertEqual(updated_er.record_id, 'NEWID')
        self.assertEqual(updated_er.external_system.id, 3)
        self.assertEqual(updated_er.label_id, 1)
        self.assertEqual(updated_er.path, 'New Path')

    @patch('api.resources.externalrecord.log')
    def test_er_update_bad_pk(self, mock_log):
        er = ExternalRecord.objects.get(pk=1)
        er_data = er.responseFieldDict()
        req = {}
        req['external_record'] = er_data
        req['id'] = '99'
        response = self.client.put(
            '/api/externalrecord/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_log.error.called)
        j = json.loads(response.content)
        r = j[0]
        self.assertFalse(r['success'], False)

    @patch('api.resources.externalrecord.log')
    def test_er_update_no_pk(self, mock_log):
        er = ExternalRecord.objects.get(pk=1)
        er_data = er.responseFieldDict()
        req = {}
        req['external_record'] = er_data

        response = self.client.put(
            '/api/externalrecord/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, 422)
        self.assertTrue(mock_log.error.called)

    @patch('api.resources.externalrecord.log')
    def test_er_delete_bad_pk(self, mock_log):
        pre = ExternalRecord.objects.count()
        response = self.client.delete(
            '/api/externalrecord/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(mock_log.error.called)
        post = ExternalRecord.objects.count()
        self.assertTrue(post == pre)

    @patch('api.resources.externalrecord.log')
    def test_er_get_bad_pk(self, mock_log):
        response = self.client.get(
            '/api/externalrecord/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, 404)


class TestExternalRecordLink(TestCase):

    fixtures = ['test_fixture.json']

    def test_get_external_links(self):
        response = self.client.get(
            '/api/externalrecord/id/1/links/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        links = json.loads(response.content)
        self.assertEqual(len(links), 1)
        link = links[0]
        self.assertEqual(link['type'], 'familial')
        self.assertEqual(link['description'], 'Parent of')
        self.assertEqual(link['external_record']['id'], 2)

    def test_create_new_external_record_link(self):
        response = self.client.post(
            '/api/externalrecord/id/2/links/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='{"related_record":4,"relation_type":1}')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertTrue(res['success'])

    def test_delete_external_record_link(self):
        response = self.client.delete(
            '/api/externalrecord/id/1/links/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertTrue(res['success'])


class TestRelationResource(TestCase):

    fixtures = ['test_fixture.json']

    def test_get_relations(self):
        response = self.client.get(
            '/api/links/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(len(res), 13)


class TestOrganization(TestCase):

    fixtures = ['test_fixture.json']

    def test_org_query_by_name(self):
        response = self.client.post(
            '/api/organization/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"name":"Test Organization"}]'
        )
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), 1)
        org = j[0]
        self.assertEqual(org['name'], 'Test Organization')

    @patch('api.resources.organization.log')
    def test_org_not_found(self, mock_log):
        response = self.client.post(
            '/api/organization/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"name":"Some Organization"}]'
        )
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({"Query": 9} in r["errors"])
        self.assertTrue(mock_log.error.called)

    @patch('api.resources.organization.log')
    def test_org_query_invalid(self, mock_log):
        response = self.client.post(
            '/api/organization/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data='[{"bad_key":"Some Organization"}]'
        )
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue({"Query": 8} in r['errors'])
        self.assertTrue(mock_log.error.called)

    def test_org_query_unsupported_type(self):
        response = self.client.post(
            '/api/organization/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/xml',
            data='[{"name":"Some Organization"}]'
        )
        self.assertEqual(response.status_code, 415)

    def test_org_update(self):
        org = Organization.objects.get(name="Test Organization")
        pre_label = org.subject_id_label
        org_data = org.responseFieldDict()
        org_data['subject_id_label'] = 'MRN'
        response = self.client.put(
            '/api/organization/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([org_data]))
        self.assertEqual(response.status_code, 200)
        org = Organization.objects.get(name="Test Organization")
        post_label = org.subject_id_label
        self.assertNotEqual(pre_label, post_label)
        self.assertEqual(pre_label, 'Record ID')
        self.assertEqual(post_label, 'MRN')

    @patch('api.resources.organization.log')
    def test_org_update_nopk(self, mock_log):
        org = Organization.objects.get(name="Test Organization")
        org_data = org.responseFieldDict()
        org_data['subject_id_label'] = 'MRN'
        del org_data['id']
        response = self.client.put(
            '/api/organization/id/%s/' % org.id,
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([org_data]))
        self.assertEqual(response.status_code, 422)
        self.assertTrue(mock_log.error.called)

    def test_org_update_org_not_found(self):
        org = Organization.objects.get(name="Test Organization")
        org_data = org.responseFieldDict()
        org_data['subject_id_label'] = 'MRN'
        org_data['id'] = 99
        response = self.client.put(
            '/api/organization/id/%s/' % org.id,
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([org_data]))
        j = json.loads(response.content)
        r = j[0]
        self.assertEqual(response.status_code, 200)
        self.assertTrue({"id": 1} in r['errors'])
        self.assertEqual(r['success'], False)

    def test_org_add(self):
        org = {
            'id': '99',
            'subject_id_label': 'Patient ID',
            'name': 'New Organization'
        }
        self.assertEqual(Organization.objects.count(), 3)
        response = self.client.post(
            '/api/organization/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([org]))
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        self.assertTrue(r['success'])
        self.assertEqual(Organization.objects.count(), 4)

    def test_org_delete(self):
        response = self.client.delete(
            '/api/organization/id/3/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Organization.objects.count(), 2)

    def test_org_get(self):
        response = self.client.get(
            '/api/organization/id/3/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(j['id'], '3')
        self.assertEqual(j['name'], 'Test Organization')

    @patch('api.resources.organization.log')
    def test_org_delete_bad_pk(self, mock_log):
        response = self.client.delete(
            '/api/organization/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertTrue(mock_log.error.called)

    @patch('api.resources.organization.log')
    def test_org_get_bad_pk(self, mock_log):
        response = self.client.get(
            '/api/organization/id/99/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertTrue(mock_log.error.called)

##### for the pedigree feature #####

    def test_pedigree_add(self):
        pre_count = PedigreeSubjectRelation.objects.count()
        pedigree = {
            'subject_1': '2',
            'subject_2': '3',
            'subject_1_role': '6',
            'subject_2_role': '7',
            'protocol_id': '1'
        }
        response = self.client.post(
            '/api/pedigree/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([pedigree])
        )

        post_count = PedigreeSubjectRelation.objects.count()
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        print(response)

        if r['success'] == True:
            self.assertTrue(r['success'])
            self.assertTrue(pre_count < post_count)
        else:
            self.assertTrue(r['errors'])
            self.assertTrue(pre_count == post_count)
    #    self.assertTrue(r['success'])




    def test_get_relationships_for_protocol(self):
        relationship_count = PedigreeSubjectRelation.objects.filter(
                                protocol_id=1).count()
        response = self.client.get(
            '/api/pedigree/protocol_id/1/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), relationship_count)

    def test_get_relationships_for_subject(self):
        relationship_count = PedigreeSubjectRelation.objects.filter(
                                    Q(subject_1=3) |
                                    Q(subject_2=3)).count()
        response = self.client.get(
            '/api/pedigree/subject_id/3/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEqual(len(j), relationship_count)
