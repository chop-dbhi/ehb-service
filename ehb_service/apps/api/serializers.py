from django.contrib.auth.models import User, Group
from rest_framework import serializers

# from api.models.protocols import Organization, DataSource, Protocol,\
#     ProtocolDataSource, ProtocolDataSourceLink, ProtocolUser,\
#     ProtocolUserCredentials


from core.models.identities import Subject, Organization, Group, SubjectGroup, ExternalSystem, ExternalRecord, ExternalRecordGroup

class SubjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        # fields = ('first_name', 'last_name', 'created', 'dob', 'modified', 'organization_id_label', 'organization_subject_id', 'organization', 'id')

class OrganizationSerializer (serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        # fields = ('id', 'subject_id_label', 'name', 'modified', 'created')

class ExternalSystemSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExternalSystem
        fields = ('description','created', 'url', 'modified', 'id', 'name')

class ExternalRecordSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExternalRecord
        fields = ('created', 'modified', 'label', 'record_id', 'path', 'external_system', 'id', 'subject')


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups', 'first_name', 'last_name')
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url',)
#
#
# class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Organization
#         fields = ('id', 'name', 'subject_id_label')
#
#
# class DataSourceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = DataSource
#         fields = ('id', 'name', 'url', 'desc_help', 'description', 'ehb_service_es_id')
#
#
# class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
#     protocol_data_sources = serializers.HyperlinkedIdentityField(view_name='protocol-datasources-list')
#     subjects = serializers.HyperlinkedIdentityField(view_name='protocol-subject-list')
#     organizations = serializers.HyperlinkedIdentityField(view_name='protocol-organization-list')
#
#     class Meta:
#         model = Protocol
#         fields = ('id', 'name', 'users', 'data_sources', 'protocol_data_sources', 'subjects', 'organizations')
#
#
# class ProtocolDataSourceSerializer(serializers.HyperlinkedModelSerializer):
#     subjects = serializers.HyperlinkedIdentityField(view_name='pds-subject-list')
#
#     class Meta:
#         model = ProtocolDataSource
#         fields = ('id', 'protocol', 'data_source', 'path', 'driver', 'driver_configuration',
#                   'display_label', 'max_records_per_subject', 'subjects')
#
#
# class ProtocolDataSourceLinkSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ProtocolDataSourceLink
#
#
# class ProtocolUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ProtocolUser
#
#
# class ProtocolUserCredentialsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = ProtocolUserCredentials
#
#
# class eHBOrganizationSerializer(serializers.Serializer):
#     """
#     This serializer corresponds to the definition of an eHB Organization
#
#     see:
#     https://github.com/chop-dbhi/ehb-service/blob/master/ehb_service/apps/core/models/identities.py
#
#     and its requested representation:
#
#     see:
#     https://github.com/chop-dbhi/ehb-client/blob/master/ehb_client/requests/organization_request_handler.py
#     """
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     subject_id_label = serializers.CharField(max_length=50)
#     created = serializers.DateTimeField()
#     modified = serializers.DateTimeField()
#
#
# class eHBSubjectSerializer(serializers.Serializer):
#     """
#     This serializer corresponds to the definition of an eHB subject
#
#     see: https://github.com/chop-dbhi/ehb-service/blob/master/ehb_service/apps/core/models/identities.py
#
#     and its requested representation:
#
#     see: https://github.com/chop-dbhi/ehb-client/blob/master/ehb_client/requests/subject_request_handler.py
#     """
#     id = serializers.IntegerField()
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=70)
#     # organization_id is PK for org in ehb-service
#     organization_id = serializers.IntegerField()
#     organization_subject_id = serializers.CharField(max_length=120)
#     organization_id_label = serializers.CharField(max_length=120)
#     dob = serializers.DateField()
#     modified = serializers.DateTimeField()
#     created = serializers.DateTimeField()
#
#
# class eHBExternalRecordSerializer(serializers.Serializer):
#     record_id = serializers.CharField(max_length=120)
#     subject_id = serializers.IntegerField()
#     external_system_id = serializers.IntegerField()
#     modified = serializers.DateTimeField()
#     created = serializers.DateTimeField()
#     path = serializers.CharField(max_length=120)
#     id = serializers.IntegerField()
#     label_id = serializers.IntegerField()
