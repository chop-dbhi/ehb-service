from django.conf.urls import url, include  # noqa
from api.resources import subject, relation, organization, group, externalsystem,externalrecord

subject_patterns = ([
    # 'api.resources.subject',
    url(r'^$', subject.SubjectResource),
    url(r'^id/(?P<pk>\d+)/$', subject.SubjectResource),
    url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', subject.SubjectResource),
    url(r'^externalrecsys/(?P<externalrecsys>\d+)/erid/(?P<erid>.*)/$', subject.SubjectResource),],
    'api')

organization_patterns = ([
    # 'api.resources.organization',
    url(r'^$', organization.OrganizationResource),
    url(r'^id/(?P<pk>\d+)/$', organization.OrganizationResource),
    url(r'^query/$', organization.OrganizationQuery),],
    'api')

externalSystem_patterns = ([
    # 'api.resources.externalsystem',
    url(r'^$', externalsystem.ExternalSystemResource),
    url(r'^id/(?P<pk>\d+)/$', externalsystem.ExternalSystemResource),
    url(r'^id/(?P<pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/subjects/$', externalsystem.ExternalSystemSubjects),
    url(r'^id/(?P<pk>\d+)/records/$', externalsystem.ExternalSystemRecords),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/records/$', externalsystem.ExternalSystemRecords),
    url(r'^query/$', externalsystem.ExternalSystemQuery),],
    'api')

externalRecord_patterns = ([
    # 'api.resources.externalrecord',
    url(r'^$', externalrecord.ExternalRecordResource),
    url(r'^id/(?P<pk>\d+)/$', externalrecord.ExternalRecordResource),
    url(r'^id/(?P<pk>\d+)/links/$', externalrecord.ExternalRecordRelationResource),
    url(r'^id/(?P<pk>\d+)/links/(?P<link>\d+)/$', externalrecord.ExternalRecordRelationResource),
    url(r'^query/$', externalrecord.ExternalRecordQuery),
    url(r'^labels/$', externalrecord.ExternalRecordLabelResource),
    url(r'^labels/(?P<pk>\d+)/$', externalrecord.ExternalRecordLabelResource),],
    'api')

group_patterns = ([
    # 'api.resources.group',
    url(r'^$', group.GroupResource),
    url(r'^id/(?P<pk>\d+)/subjects/$', group.SubjectGroupResource),
    url(r'^id/(?P<grp_pk>\d+)/subjects/id/(?P<x_pk>\d+)/$', group.SubjectGroupResource),
    url(r'^id/(?P<pk>\d+)/records/$', group.RecordGroupResource),
    url(r'^id/(?P<grp_pk>\d+)/records/id/(?P<x_pk>\d+)/$', group.RecordGroupResource),],
    'api')

pedigreeRelationship_patterns = ([
    # 'api.resources.relation',
    url(r'^$', relation.PedigreeSubjectRelationResource),
    url(r'^protocol_id/(?P<protocol_id>\d+)/$', relation.PedigreeSubjectRelationResource),
    url(r'^subject_id/(?P<subject_id>\d+)/$', relation.PedigreeSubjectRelationResource),],
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
    url(r'^links/$', relation.RelationResource),
    url(r'^pedigree/', include(pedigreeRelationship_patterns,
        namespace='pedigree')),
]
