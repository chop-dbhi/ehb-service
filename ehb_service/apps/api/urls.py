from django.conf.urls import *  # noqa

subject_patterns = patterns(
    'api.resources.subject',
    url(r'^$', 'SubjectResource'),
    url(r'^id/(?P<pk>\d+)/$', 'SubjectResource'),
    url(r'^organization/(?P<org_pk>\d+)/osid/(?P<osid>\w+)/$', 'SubjectResource'),
)

organization_patterns = patterns(
    'api.resources.organization',
    url(r'^$', 'OrganizationResource'),
    url(r'^id/(?P<pk>\d+)/$', 'OrganizationResource'),
    url(r'^query/$', 'OrganizationQuery'),
)

externalSystem_patterns = patterns(
    'api.resources.externalsystem',
    url(r'^$', 'ExternalSystemResource'),
    url(r'^id/(?P<pk>\d+)/$', 'ExternalSystemResource'),
    url(r'^id/(?P<pk>\d+)/subjects/$', 'ExternalSystemSubjects'),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/subjects/$', 'ExternalSystemSubjects'),
    url(r'^id/(?P<pk>\d+)/records/$', 'ExternalSystemRecords'),
    url(r'^id/(?P<pk>\d+)/organization/(?P<org_pk>\d+)/records/$', 'ExternalSystemRecords'),
    url(r'^query/$', 'ExternalSystemQuery'),
)

externalRecord_patterns = patterns(
    'api.resources.externalrecord',
    url(r'^$', 'ExternalRecordResource'),
    url(r'^id/(?P<pk>\d+)/$', 'ExternalRecordResource'),
    url(r'^id/(?P<pk>\d+)/links/$', 'ExternalRecordRelationResource'),
    url(r'^query/$', 'ExternalRecordQuery'),
    url(r'^labels/$', 'ExternalRecordLabelResource'),
    url(r'^labels/(?P<pk>\d+)/$', 'ExternalRecordLabelResource'),
)

group_patterns = patterns(
    'api.resources.group',
    url(r'^$', 'GroupResource'),
    url(r'^id/(?P<pk>\d+)/subjects/$', 'SubjectGroupResource'),
    url(r'^id/(?P<grp_pk>\d+)/subjects/id/(?P<x_pk>\d+)/$', 'SubjectGroupResource'),
    url(r'^id/(?P<pk>\d+)/records/$', 'RecordGroupResource'),
    url(r'^id/(?P<grp_pk>\d+)/records/id/(?P<x_pk>\d+)/$', 'RecordGroupResource'),
)

urlpatterns = patterns(
    '',
    url(r'^subject/', include(subject_patterns, namespace='subject')),
    url(r'^externalsystem/', include(externalSystem_patterns, namespace='externalsystem')),
    url(r'^externalrecord/', include(externalRecord_patterns, namespace='externalrecord')),
    url(r'^organization/', include(organization_patterns, namespace='organization')),
    url(r'^group/', include(group_patterns, namespace='group')),
    url(r'^links/$', 'api.resources.relation.RelationResource'),

)
