from django.conf.urls import url, include  # noqa
from api.views import subject, relation, organization, group, externalsystem,externalrecord

subject_patterns = ([
    # 'api.resources.subject',
    url(r'^$', subject.SubjectResource.as_view()),
    url(r'^id/(?P<pk>\d+)/$', subject.SubjectResource.as_view()),
    url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', subject.SubjectResource.as_view()),
    url(r'^externalrecsys/(?P<externalrecsys>\d+)/erid/(?P<erid>.*)/$', subject.SubjectResource.as_view()),],
    'api')

organization_patterns = ([
    # 'api.resources.organization',
    url(r'^$', organization.OrganizationResource.as_view()),
    url(r'^id/(?P<pk>\d+)/$', organization.OrganizationResource.as_view()),
    url(r'^query/$', organization.OrganizationQuery.as_view()),],
    'api')

externalSystem_patterns = ([
    # 'api.resources.externalsystem',
    url(r'^$', externalsystem.ExternalSystemResource.as_view()),
    url(r'^id/(?P<pk>\d+)/$', externalsystem.ExternalSystemResource.as_view()),
    url(r'^id/(?P<pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects.as_view()),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects.as_view()),
    url(r'^id/(?P<pk>\d+)/records/$', externalsystem.ExternalSystemRecords.as_view()),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/records/$', externalsystem.ExternalSystemRecords.as_view()),
    url(r'^query/$', externalsystem.ExternalSystemQuery.as_view()),],
    'api')

externalRecord_patterns = ([
    # 'api.resources.externalrecord',
    url(r'^$', externalrecord.ExternalRecordResource.as_view()),
    url(r'^id/(?P<pk>\d+)/$', externalrecord.ExternalRecordResource.as_view()),
    url(r'^id/(?P<pk>\d+)/links/$', externalrecord.ExternalRecordRelationResource.as_view()),
    url(r'^id/(?P<pk>\d+)/links/(?P<link>\d+)/$', externalrecord.ExternalRecordRelationResource.as_view()),
    url(r'^query/$', externalrecord.ExternalRecordQuery.as_view()),
    url(r'^labels/$', externalrecord.ExternalRecordLabelResource.as_view()),
    url(r'^labels/(?P<pk>\d+)/$', externalrecord.ExternalRecordLabelResource.as_view()),],
    'api')

group_patterns = ([
    # 'api.resources.group',
    url(r'^$', group.GroupResource.as_view()),
    url(r'^id/(?P<pk>\d+)/subjects/$', group.SubjectGroupResource.as_view()),
    url(r'^id/(?P<grp_pk>\d+)/subjects/id/(?P<x_pk>\d+)/$', group.SubjectGroupResource.as_view()),
    url(r'^id/(?P<pk>\d+)/records/$', group.RecordGroupResource.as_view()),
    url(r'^id/(?P<grp_pk>\d+)/records/id/(?P<x_pk>\d+)/$', group.RecordGroupResource.as_view()),],
    'api')

pedigreeRelationship_patterns = ([
    # 'api.resources.relation',
    url(r'^$', relation.PedigreeSubjectRelationResource.as_view()),
    url(r'^protocol_id/(?P<protocol_id>\d+)/$', relation.PedigreeSubjectRelationResource.as_view()),
    url(r'^subject_id/(?P<subject_id>\d+)/$', relation.PedigreeSubjectRelationResource.as_view()),],
    'api')
    #url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', 'PedigreeSubjectRelationResource'),

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
    url(r'^links/$', relation.RelationResource.as_view()),
    url(r'^pedigree/', include(pedigreeRelationship_patterns,
        namespace='pedigree')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
