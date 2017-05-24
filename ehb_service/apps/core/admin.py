'''
Created on May 17, 2011

@author: masinoa
'''
from models.identities import (
    Subject,
    SubjectValidation,
    ExternalSystem,
    ExternalRecord,
    Group,
    SubjectGroup,
    ExternalRecordGroup,
    Organization,
    ExternalRecordRelation,
    Relation,
    ExternalRecordLabel
)
from models.clients import MachineClient
from django.contrib import admin

class SubjectAdmin(admin.ModelAdmin):
    list_filter = ['organization', 'created', 'modified']
    # Search Field does not work due to encryption. need to override query
    search_fields = ['organization__name', 'last_name', 'organization_subject_id']
    list_display = ['last_name', 'first_name', 'organization', 'organization_subject_id']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectValidation)
admin.site.register(ExternalRecordRelation)
admin.site.register(Relation)
admin.site.register(ExternalRecordLabel)

class ExternalSystemAdmin(admin.ModelAdmin):
    list_filter = ['created', 'modified']
    search_fields = ['name']
    list_display = ['name', 'url', 'description']

admin.site.register(ExternalSystem, ExternalSystemAdmin)

class ExternalRecordAdmin(admin.ModelAdmin):
    list_filter = ['external_system', 'created']
    list_display = ['subject', 'external_system', 'path', 'record_id']
    # need to overide this search query to decrypt subject field
    search_fields = ['subject__last_name']
    raw_id_fields = ['subject', 'external_system']

admin.site.register(ExternalRecord, ExternalRecordAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']
    list_display = ['name', 'subject_id_label']

admin.site.register(Organization, OrganizationAdmin)

class SubjectGroupAdmin(admin.ModelAdmin):
    list_filter = ['group']
    # need to overide this search query to decrypt subject field
    search_fields = ['group__name']
    list_display = ['group']
    readonly_fields = ['subjects', 'group']

admin.site.register(SubjectGroup, SubjectGroupAdmin)

class ExternalRecordGroupAdmin(admin.ModelAdmin):
    list_filter = ['group']
    # need to overide this search query to decrypt subject field
    search_fields = ['group__name']
    list_display = ['group']

admin.site.register(ExternalRecordGroup, ExternalRecordGroupAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['name']
    list_display = ['name', 'is_locking', 'description', 'created', 'modified']

    def get_actions(self, request):
        '''prevent bulk deletes'''
        actions = super(GroupAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        '''prevent item level deletes'''
        return False

admin.site.register(Group, GroupAdmin)

class MachineClientAdmin(admin.ModelAdmin):
    list_filter = ['ip_address', 'host_name']
    search_fields = list_filter
    list_display = list_filter

admin.site.register(MachineClient, MachineClientAdmin)
