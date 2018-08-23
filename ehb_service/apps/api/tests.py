"""
Run via Django's manage.py tool: `./bin/manage.py test api`
"""
import json

from core.models.identities import Organization, Subject, Group, ExternalRecord, ExternalSystem
from django.test import TestCase

from mock import patch

from parameterized import parameterized


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

    # TODO make names more explicit and remove from class
    def assert_success(self, j):
        self.assertTrue(j[0]['success'])

    def assert_no_errors(self, j):
        self.assertFalse(j[0]['errors'], 13)

    def assert_not_success(self, j):
        self.assertFalse(j[0]['success'])

    def assert_errors(self, j):
        self.assertTrue(j[0]['errors'], 13)

    def assert_len(self, j):
        self.assertEqual(len(j), 1)

    @parameterized.expand([
        ('/api/group/', 'application/json', 'name=BRP:NEWTESTGROUP', None, 'secretkey123', 403),  # no client key
        ('/api/group/', 'application/json', None, 'testck', 'secretkey123', 400),  # no query string
        ('/api/group/', 'application/json', 'name=BAD', 'testck', 'secretkey123', 404),  # bad query string
    ])
    @patch('api.resources.group.log')
    def test_delete_group_patched(self, path, content_type, query_string, client_key, api_token, response_code,
                                  mock_log):
        self.base_delete_group(path, content_type, query_string, client_key, api_token, response_code, mock_log)

    @parameterized.expand([
        ('/api/group/', 'application/json', 'id=6', 'testck', "secretkey123", 204),  # via client key
        ('/api/group/', 'application/json', 'name=BRP:NEWTESTGROUP', 'testck', "secretkey123", 204),  # via name
    ])
    def test_delete_group(self, path, content_type, query_string, client_key, api_token, response_code):
        self.base_delete_group(path, content_type, query_string, client_key, api_token, response_code)

    def base_delete_group(self, path, content_type, query_string, client_key, api_token, response_code, mock_log=None):
        pre_count = Group.objects.count()
        response = self.client.delete(
            path,
            content_type=content_type,
            QUERY_STRING=query_string,
            HTTP_GROUP_CLIENT_KEY=client_key,
            HTTP_API_TOKEN=api_token)
        post_count = Group.objects.count()
        self.assertEqual(response.status_code, response_code)
        self.assertTrue(post_count < pre_count if mock_log is None else mock_log.error.called)

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

    @parameterized.expand([
        ('6', 'BRP:NEWTESTGROUP', 'testck', 200, '6', [assert_success])
    ])
    def test_update_group(self, inner_id, name, current_client_key, expected_error_code, outer_id, assertions):
        self.base_update_group(inner_id, name, current_client_key, expected_error_code, outer_id, assertions)

    @parameterized.expand([
        ('2', 'BRP:M0536B4E2DDLA7W6', 'testck', 400, None, None),  # no pk
        ('2', 'BRP:NEWTESTGROUP', 'BADCK', 401, '2', None),  # bad ck
        ('1', 'BRP:NEWTESTGROUP', None, 400, '1', None),  # no ck
        ('99', 'BRP:M0536B4E2DDLA7W6', 'testck', 200, '99', [assert_not_success])  # bad pk
    ])
    @patch('api.resources.group.log')
    def test_update_group_patched(self, inner_id, name, client_key, error_code, outer_id, assertions, mock_log):
        self.base_update_group(inner_id, name, client_key, error_code, outer_id, assertions, mock_log)

    def base_update_group(self, inner_id, name, client_key, error_code, outer_id, additional_assertions, mock_log=None):
        req = {
            'id': outer_id,
            'group': {
                'description': 'A New Desciption',
                'id': inner_id,
                'is_locking': 'True',
                'name': name,
                'current_client_key': client_key
            }
        }
        if outer_id is None:
            del req['id']
        response = self.client.put(
            '/api/group/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))

        if mock_log is not None:
            self.assertTrue(mock_log.error.called)
        self.assertEqual(response.status_code, error_code)
        if additional_assertions is not None:
            j = json.loads(response.content)
            for assertion in additional_assertions:
                assertion(self, j)

    @parameterized.expand([
        ('6', '[4]', 'testck', 200, [assert_success], True),
    ])
    def test_add_record_to_group(self, response_id, data, client_key, status_code, additional_assertions, get_pk):
        self.base_add_record_to_group(response_id, data, client_key, status_code, additional_assertions, get_pk)

    @parameterized.expand([
        ('99', json.dumps([2]), 'testck', 404, None),  # no group
        ('6', '[2]', None, 403, None),  # no ck
        ('6', json.dumps([99]), 'testck', 200, [assert_not_success, assert_errors]),  # bad record id
    ])
    @patch('api.resources.group.log')
    def test_add_record_to_group_patched(self, response_id, data, client_key, status_code, assertions, mock_log):
        self.base_add_record_to_group(response_id, data, client_key, status_code, assertions, False, mock_log)

    def base_add_record_to_group(self, response_id, data, client_key, status_code, assertions, get_pk, mock_log=None):
        if get_pk:
            er = Group.objects.get(pk=6).externalrecordgroup_set.all()
        response = self.client.post(
            '/api/group/id/{0}/records/'.format(response_id),
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=data,
            HTTP_GROUP_CLIENT_KEY=client_key)
        self.assertEqual(response.status_code, status_code)
        if assertions is not None:
            j = json.loads(response.content)
            for assertion in assertions:
                assertion(self, j)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)

    def test_delete_record(self):
        self.base_delete_record('6', '2', 'testck', 204)

    @parameterized.expand([
        ('3', '1', 'BADKEY', 403),  # bad key
        ('99', '1', 'testck', 404),  # bad x
        ('6', '99', 'testck', 404),  # no xg
    ])
    @patch('api.resources.group.log')
    def test_delete_record_patched(self, id1, id2, client_key, expected_status_code, mock_log):
        self.base_delete_record(id1, id2, client_key, expected_status_code, mock_log)

    def base_delete_record(self, id1, id2, client_key, expected_status_code, mock_log=None):
        response = self.client.delete(
            '/api/group/id/{0}/records/id/{1}/'.format(id1, id2),
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            HTTP_GROUP_CLIENT_KEY=client_key)
        self.assertEqual(response.status_code, expected_status_code)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)

    @parameterized.expand([
        ('?name=BRP:NEWTESTGROUP', 'testck', 200, ['id', '6'], None),  # protocol by name
        ('?id=2', 'testck', 200, ['name', 'BRP:M0536B4E2DDLA7W6'], None),  # protocol by id
        ('id/6/records/', 'testck', 200, None, [assert_len]),  # group records
        ('id/7/subjects/', 'testck', 200, None, [assert_len]),  # group subjects
        ('id/2/subjects/', 'BADKEY', 403, None, None)  # group subjects bad ck
    ])
    def test_get(self, api_group, client_key, expected_status_code, equal_assertion, additional_assertions):
        self.base_get(api_group, client_key, expected_status_code, equal_assertion, additional_assertions)

    @parameterized.expand([
        ('?name=BADGROUP', 'testck', 416, None, None),  # protocol by name bad group
        ('id/8/records/', 'testck', 404, None, None),  # group records no group provided
        ('id/99/subjects/', 'testck', 404, None, None)  # bad group subject id
    ])
    @patch('api.resources.group.log')
    def test_get_patched(self, api_group, client_key, expected_status_code, equal_assertion, additional_assertions,
                         mock_log):
        self.base_get(api_group, client_key, expected_status_code, equal_assertion, additional_assertions, mock_log)

    def base_get(self, api_group, client_key, expected_status_code, equal_assertion, additional_assertions,
                 mock_log=None):
        response = self.client.get(
            '/api/group/{0}'.format(api_group), **{
                "CONTENT_TYPE": 'application/json',
                "HTTP_GROUP_CLIENT_KEY": client_key,
                'HTTP_API_TOKEN': 'secretkey123'
            }
        )
        self.assertEqual(response.status_code, expected_status_code)
        if equal_assertion is not None:
            j = json.loads(response.content)
            self.assertEqual(j[equal_assertion[0]], equal_assertion[1])
        if additional_assertions is not None:
            j = json.loads(response.content)
            for assertion in additional_assertions:
                assertion(self, j)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)


class TestSubject(TestCase):
    fixtures = ['test_fixture.json']

    # TODO make method names more explicit and remove from class

    @staticmethod
    def assert_success(provided_self, test_case_output):
        provided_self.assertTrue(test_case_output[0]['success'])

    @staticmethod
    def assert_no_errors(provided_self, test_case_output):
        provided_self.assertFalse(test_case_output[0]['errors'], 13)

    @staticmethod
    def assert_not_success(provided_self, test_case_output):
        provided_self.assertFalse(test_case_output[0]['success'])

    @staticmethod
    def assert_errors(provided_self, test_case_output):
        provided_self.assertTrue(test_case_output[0]['errors'], 13)

    @parameterized.expand([
        ('id/2/'),  # default
        ('organization/3/osid/123456/'),  # by osid
    ])
    def test_subject_get(self, api_subject):
        self.base_subject_get(api_subject, 200, True)

    @parameterized.expand([
        ('id/99/'),  # bad pk
        ('organization/99/osid/123456/'),  # by_osid_bad_org
        ('organization/3/osid/99/'),  # get ocid bad ocid
    ])
    @patch('api.resources.subject.log')
    def test_subject_get_patched(self, api_subject, mock_log):
        self.base_subject_get(api_subject, 404, False, mock_log)

    def base_subject_get(self, api_subject, status_code, assess_equal, mock_log=None):
        response = self.client.get(
            '/api/subject/{0}'.format(api_subject),
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)
        if assess_equal:
            j = json.loads(response.content)
            self.assertEqual(j['first_name'], 'John')
            self.assertEqual(j['last_name'], 'Doe')
            self.assertEqual(j['dob'], '2000-01-01')
            self.assertEqual(j['organization'], 3)
            self.assertEqual(j['organization_subject_id'], '123456')

    def test_subject_delete(self):
        pre_count = Subject.objects.count()
        response = self.client.delete(
            '/api/subject/id/2/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json')
        post_count = Subject.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertTrue(post_count < pre_count)

    @parameterized.expand([
        '999999',
        '123456'
    ])
    def test_subject_add(self, subject_id):
        pre_count = Subject.objects.count()
        sub = {
            'first_name': 'New',
            'last_name': 'Subject',
            'dob': '2000-01-01',
            'organization': '3',
            'organization_subject_id': subject_id
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
        if subject_id == '999999':
            self.assertTrue(r['success'])
            self.assertTrue(pre_count < post_count)
        else:
            self.assertTrue({"__all__": 3} in r['errors'])

    def test_subject_update(self):
        self.base_subject_update(0, 0, 200, TestSubject.assert_success, None, True)

    @parameterized.expand([
        (1, 200, assert_not_success, {"id": 1}, False),
        (2, 400, None, None, False)
    ])
    @patch('api.resources.subject.log')
    def test_subject_update_patched(self, id_type, status_code, success_assessment, assert_in_errors, assert_whole,
                                    mock_log):
        self.base_subject_update(id_type, 0, status_code,
                                 None if success_assessment is None else success_assessment.__func__,
                                 assert_in_errors, assert_whole, mock_log)

    @parameterized.expand([
        ('', assert_not_success)
        # arbitrary parameter required to force python to interpret as tuple instead of function
    ])
    @patch('api.helpers.log')
    def test_subject_update_patched_helpers(self, _, success_assertion, mock_log):
        self.base_subject_update(0, 1, 200, success_assertion.__func__, {"organization": 7}, False, mock_log)

    def base_subject_update(self, id_type, organization_type, status_code, success_assessment, assert_in_errors,
                            assert_whole,
                            mock_log=None):
        sub = Subject.objects.get(pk=2)
        pre_id = sub.organization_subject_id
        sub_data = sub.responseFieldDict()
        sub_data['organization_subject_id'] = '999999'
        sub_data['organization'] = sub.organization_id if organization_type == 0 else '99'
        req = {'new_subject': sub_data, 'id': sub.id if id_type == 0 else '99' if id_type == 1 else None}
        response = self.client.put(
            '/api/subject/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        sub = Subject.objects.get(pk=2)
        self.assertEqual(response.status_code, status_code)
        if success_assessment is not None:
            j = json.loads(response.content)
            success_assessment(self, j)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)
        if assert_in_errors is not None:
            j = json.loads(response.content)
            r = j[0]
            self.assertTrue(assert_in_errors, r['errors'])
        if assert_whole:
            self.assertEqual(sub.organization_subject_id, '999999')
            self.assertTrue(pre_id != sub.organization_subject_id)


class TestExternalSystem(TestCase):
    fixtures = ['test_fixture.json']

    @parameterized.expand([
        '[{"name":"Nautilus Test"}]',  # by name
        '[{"url":"http://nautilus.local:8090/api/"}]'  # by url
    ])
    def test_es_query(self, data):
        self.base_es_query(data, None, {'name': 'Nautilus Test', 'url': 'http://nautilus.local:8090/api/'})

    @parameterized.expand([
        ('[{"name":"Bad Name"}]', {'Query': 9}),  # by name not found
        ('[{"url":"http://badurl.local: 8090/api/"}]', {'Query': 9}),  # by url not found
        ('[{"bad_param":""}]', {'Query': 8})  # invalid query
    ])
    @patch('api.resources.externalsystem.log')
    def test_es_query_patched(self, data, assert_in_errors, mock_log):
        self.base_es_query(data, assert_in_errors, None, mock_log)

    def base_es_query(self, data, assert_in_errors, equal_assertions, mock_log=None):
        response = self.client.post(
            '/api/externalsystem/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=data)
        self.assertEqual(response.status_code, 200)
        j = json.loads(response.content)
        r = j[0]
        if equal_assertions is not None:
            for key in equal_assertions:
                self.assertTrue(r['externalSystem'][key], equal_assertions[key])
        if assert_in_errors is not None:
            self.assertTrue(assert_in_errors, r['errors'])
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)

    @parameterized.expand([
        ('id/2/subjects/', True, True),  # subjects
        ('id/2/organization/3/subjects/', False, True),  # subjects by org
        ('id/2/records/', True, True),  # exrecs
        ('id/2/organization/3/records/', True, True),  # exrecs by org
    ])
    def test_es_xref(self, external_system, include_content, test_length):
        self.base_es_xref(external_system, 200, include_content, test_length)

    @parameterized.expand([
        ('id/2/organization/99/subjects/', False, False),  # subjects by bad org
        ('id/99/organization/3/subjects/', False, False),  # subjects by bad es
        ('id/2/organization/99/records/', True, False),  # exrecs by bad org
        ('id/99/records/', True, False)  # exrecs by bad es
    ])
    @patch('api.resources.externalsystem.log')
    def test_es_xref_patched(self, external_system, include_content, test_length, mock_log):
        self.base_es_xref(external_system, 404, include_content, test_length, mock_log)

    def base_es_xref(self, external_system, status_code, include_content, test_length, mock_log=None):
        response = self.client.get(
            '/api/externalsystem/{0}'.format(external_system),
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json' if include_content else None
        )
        self.assertEqual(response.status_code, status_code)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)
        if test_length:
            j = json.loads(response.content)
            self.assertEqual(len(j), 2)

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
        self.base_es_update(0, 200, True, True, False, True)

    @parameterized.expand([
        (1, 200, False, False, True, True),  # bad id
        (0, 400, None, False, False, False)  # bad query
    ])
    @patch('api.resources.externalsystem.log')
    def test_es_update_patched(self, id_source, status_code, success_assertion, assert_names, assert_in_errors,
                               get_from_es, mock_log):
        self.base_es_update(id_source, status_code, success_assertion, assert_names, assert_in_errors, get_from_es,
                            mock_log)

    def base_es_update(self, id_source, status_code, success_assertion, assert_names, assert_in_errors, get_from_es,
                       mock_log=None):
        req = {}
        pre_name = None
        req['external_system'] = None
        if get_from_es:
            es = ExternalSystem.objects.get(pk=2)
            pre_name = es.name
            es_data = es.responseFieldDict()
            es_data['name'] = "New Name"
            req['external_system'] = es_data
            req['id'] = es_data['id'] if id_source is 0 else '99'
        response = self.client.put(
            '/api/externalsystem/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=json.dumps([req]))
        self.assertEqual(response.status_code, status_code)
        if success_assertion is not None:
            r = json.loads(response.content)[0]
            if success_assertion:
                self.assertTrue(r['success'])
            else:
                self.assertFalse(r['success'])
        if assert_names:
            es = ExternalSystem.objects.get(pk=2)
            self.assertTrue(pre_name != es.name)
            self.assertEqual(es.name, 'New Name')
        if assert_in_errors:
            r = json.loads(response.content)[0]
            self.assertTrue({"id": 1} in r['errors'])
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)

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

    @parameterized.expand([
        ('[{"subject_id": "2"}]', 3, None, None, 200),  # by sub id
        ('[{"subject_org": "2", "subject_id":"1"}]', None, None, None, 200),  # by sub id
        ('[{"subject_org": "3", "subject_org_id":"54545454"}]', 1, {'subject_org': '3', 'subject_org_id': '54545454'},
         None, 200),  # by sub org and sub org id
        ('[{"external_system_id":"1"}]', 2, None, ['external_system', 1], 200),  # by esid
        ('[{"external_system_name":"Nautilus Test"}]', 2, None, ['external_system', 1], 200),  # by es name
        ('[{"external_system_url":"http://nautilus.local:8090/api/"}]', 2, None, ['external_system', 1], 200),
        # by es url
        ('[{"path":"Test Protocol"}]', 4, None, ['path', 'Test Protocol'], 200),  # by path
    ])
    def test_er_query(self, data, ex_recs_len, equal_assertions, ex_recs_assertion, status_code):
        self.base_er_query(data, ex_recs_len, equal_assertions, ex_recs_assertion, status_code, None)

    @parameterized.expand([
        ('[{"subject_id": "99"}]', None, {'errors': {'Query': 9}, 'subject_id': '99'}, None, 200, None),  # bad sub id
        ('[{"external_system_id":"99"}]', None, {'errors': {'Query': 9}, 'external_system_id': '99'}, None, 200, None),
        # bad query esid
        ('[{"path": "BAD PATH"}]', None, None, None, 200, {"Query": 9}),  # bad params
    ])
    @patch('api.resources.externalrecord.log')
    def test_er_query_patched(self, data, ex_recs_len, equal_assertions, ex_recs_assertion, status_code,
                              assert_in_errors, mock_log):
        self.base_er_query(data, ex_recs_len, equal_assertions, ex_recs_assertion, status_code, assert_in_errors,
                           mock_log)

    def base_er_query(self, data, ex_recs_len, equal_assertions, ex_recs_assertion, status_code, assert_in_errors,
                      mock_log=None):
        response = self.client.post(
            '/api/externalrecord/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/json',
            data=data)
        self.assertEqual(response.status_code, status_code)
        if ex_recs_len is not None:
            j = json.loads(response.content)
            ex_recs = j[0]['external_record']
            self.assertEqual(len(ex_recs), ex_recs_len)
            if ex_recs_assertion is not None:
                for each in ex_recs:
                    self.assertEqual(each[ex_recs_assertion[0]], ex_recs_assertion[1])
        if equal_assertions is not None:
            j = json.loads(response.content)
            for key in equal_assertions:
                self.assertEqual(j[0][key], equal_assertions[key])
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)
        if assert_in_errors is not None:
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
        self.assertEqual(len(res), 2)


class TestOrganization(TestCase):
    fixtures = ['test_fixture.json']

    @parameterized.expand([
        ('[{"name":"Test Organization"}]', ['name', 'Test Organization'], None, 1, 200, 'json'),  # by name
        ('[{"name":"Some Organization"}]', None, None, None, 415, 'xml')  # unsuported type
    ])
    def test_org_query(self, data, org_assertion, assert_in_errors, assert_json_len, status_code, content_type):
        self.base_org_query(data, org_assertion, assert_in_errors, assert_json_len, status_code, content_type)

    @parameterized.expand([
        ('[{"name":"Some Organization"}]', None, {'Query': 9}, None, 200),  # not found
        ('[{"bad_key":"Some Organization"}]', None, {'Query': 8}, None, 200)  # invalid
    ])
    @patch('api.resources.organization.log')
    def test_org_query_patched(self, data, org_assertion, assert_in_errors, assert_json_len, status_code, mock_log):
        self.base_org_query(data, org_assertion, assert_in_errors, assert_json_len, status_code, 'json', mock_log)

    def base_org_query(self, data, org_assertion, assert_in_errors, assert_json_len, status_code, content_type,
                       mock_log=None):
        response = self.client.post(
            '/api/organization/query/',
            HTTP_API_TOKEN='secretkey123',
            content_type='application/{0}'.format(content_type),
            data=data)
        self.assertEqual(response.status_code, status_code)

        if org_assertion is not None:
            j = json.loads(response.content)
            r = j[0]
            self.assertEqual(r[org_assertion[0]], org_assertion[1])
        if assert_in_errors is not None:
            j = json.loads(response.content)
            r = j[0]
            self.assertTrue(assert_in_errors in r['errors'])
        if assert_json_len is not None:
            self.assertEqual(len(json.loads(response.content)), assert_json_len)
        if mock_log is not None:
            self.assertTrue(mock_log.error.called)

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
