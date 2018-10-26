from django.conf.urls import url, include  # noqa
from api.views import subject, relation, organization, group, externalsystem,externalrecord

subject_patterns = ([
    url(r'^$', subject.SubjectView.as_view()),
    url(r'^id/(?P<pk>\d+)/$', subject.SubjectView.as_view()),
    url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', subject.SubjectView.as_view()),
    url(r'^externalrecsys/(?P<externalrecsys>\d+)/erid/(?P<erid>.*)/$', subject.SubjectView.as_view()),],
    'api')

organization_patterns = ([
    url(r'^$', organization.OrganizationView.as_view()),
    url(r'^id/(?P<pk>\d+)/$', organization.OrganizationView.as_view()),
    url(r'^query/$', organization.OrganizationQuery.as_view()),],
    'api')

externalSystem_patterns = ([
    url(r'^$', externalsystem.ExternalSystemView.as_view()),
    url(r'^id/(?P<pk>\d+)/$', externalsystem.ExternalSystemView.as_view()),
    url(r'^id/(?P<pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects.as_view()),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects.as_view()),
    url(r'^id/(?P<pk>\d+)/records/$', externalsystem.ExternalSystemRecords.as_view()),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/records/$', externalsystem.ExternalSystemRecords.as_view()),
    url(r'^query/$', externalsystem.ExternalSystemQuery.as_view()),],
    'api')

externalRecord_patterns = ([
    url(r'^$', externalrecord.ExternalRecordView.as_view()),
    url(r'^id/(?P<pk>\d+)/$', externalrecord.ExternalRecordView.as_view()),
    url(r'^id/(?P<pk>\d+)/links/$', externalrecord.ExternalRecordRelationView.as_view()),
    url(r'^id/(?P<pk>\d+)/links/(?P<link>\d+)/$', externalrecord.ExternalRecordRelationView.as_view()),
    url(r'^query/$', externalrecord.ExternalRecordQuery.as_view()),
    url(r'^labels/$', externalrecord.ExternalRecordLabelView.as_view()),
    url(r'^labels/(?P<pk>\d+)/$', externalrecord.ExternalRecordLabelView.as_view()),],
    'api')

group_patterns = ([
    url(r'^$', group.GroupView.as_view()),
    url(r'^id/(?P<pk>\d+)/subjects/$', group.SubjectGroupView.as_view()),
    url(r'^id/(?P<grp_pk>\d+)/subjects/id/(?P<x_pk>\d+)/$', group.SubjectGroupView.as_view()),
    url(r'^id/(?P<pk>\d+)/records/$', group.RecordGroupView.as_view()),
    url(r'^id/(?P<grp_pk>\d+)/records/id/(?P<x_pk>\d+)/$', group.RecordGroupView.as_view()),],
    'api')

pedigreeRelationship_patterns = ([
    url(r'^$', relation.PedigreeSubjectRelationView.as_view()),
    url(r'^protocol_id/(?P<protocol_id>\d+)/$', relation.PedigreeSubjectRelationView.as_view()),
    url(r'^subject_id/(?P<subject_id>\d+)/$', relation.PedigreeSubjectRelationView.as_view()),],
    'api')
    #url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', 'PedigreeSubjectRelationView'),

urlpatterns = [
    url(r'^subject/', include(subject_patterns,
        namespace='subject')),
    url(r'^externalsystem/', include(externalSystem_patterns,
        namespace='externalsystem')),
    url(r'^externalrecord/', include(externalRecord_patterns,
        namespace='externalrecord')),
    url(r'^organization/', include(organization_patterns,
        namespace='organization')),
    url(r'^group/', include(group_patterns,
        namespace='group')),
    url(r'^links/$', relation.RelationView.as_view()),
    url(r'^pedigree/', include(pedigreeRelationship_patterns,
        namespace='pedigree')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
