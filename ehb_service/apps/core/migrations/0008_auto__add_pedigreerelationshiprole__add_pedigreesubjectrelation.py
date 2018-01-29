# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PedigreeRelationshipRole'
        db.create_table(u'core_pedigreerelationshiprole', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['PedigreeRelationshipRole'])

        # Adding model 'PedigreeSubjectRelation'
        db.create_table(u'core_pedigreesubjectrelation', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_1', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='subject_1', null=True, to=orm['core.Subject'])),
            ('subject_2', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='subject_2', null=True, to=orm['core.Subject'])),
            ('subject_1_role', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='subject_1_role', null=True, to=orm['core.PedigreeRelationshipRole'])),
            ('subject_2_role', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='subject_2_role', null=True, to=orm['core.PedigreeRelationshipRole'])),
            ('protocol_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['PedigreeSubjectRelation'])


    def backwards(self, orm):
        # Deleting model 'PedigreeRelationshipRole'
        db.delete_table(u'core_pedigreerelationshiprole')

        # Deleting model 'PedigreeSubjectRelation'
        db.delete_table(u'core_pedigreesubjectrelation')


    models = {
        u'core.externalrecord': {
            'Meta': {'object_name': 'ExternalRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ExternalSystem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['core.ExternalRecordLabel']", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'record_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"})
        },
        u'core.externalrecordgroup': {
            'Meta': {'ordering': "['group']", 'object_name': 'ExternalRecordGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_records': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.ExternalRecord']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.externalrecordlabel': {
            'Meta': {'object_name': 'ExternalRecordLabel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.externalrecordrelation': {
            'Meta': {'object_name': 'ExternalRecordRelation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_record': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'external_record'", 'null': 'True', 'to': u"orm['core.ExternalRecord']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'related_record': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'related_record'", 'null': 'True', 'to': u"orm['core.ExternalRecord']"}),
            'relation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Relation']"})
        },
        u'core.externalsystem': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExternalSystem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Subject']", 'symmetrical': 'False', 'through': u"orm['core.ExternalRecord']", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'client_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'ehb_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.GroupEhbKey']", 'unique': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('core.encryption.encryptionFields.EncryptCharField', [], {'unique': 'True', 'max_length': '232'})
        },
        u'core.groupehbkey': {
            'Meta': {'object_name': 'GroupEhbKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('core.encryption.encryptionFields.EncryptCharField', [], {'unique': 'True', 'max_length': '232', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.machineclient': {
            'Meta': {'unique_together': "(('ip_address', 'host_name'),)", 'object_name': 'MachineClient'},
            'host_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'core.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'subject_id_label': ('django.db.models.fields.CharField', [], {'default': "'Record ID'", 'max_length': '50'})
        },
        u'core.pedigreerelationshiprole': {
            'Meta': {'object_name': 'PedigreeRelationshipRole'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.pedigreesubjectrelation': {
            'Meta': {'object_name': 'PedigreeSubjectRelation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'protocol_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subject_1': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subject_1'", 'null': 'True', 'to': u"orm['core.Subject']"}),
            'subject_1_role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subject_1_role'", 'null': 'True', 'to': u"orm['core.PedigreeRelationshipRole']"}),
            'subject_2': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subject_2'", 'null': 'True', 'to': u"orm['core.Subject']"}),
            'subject_2_role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subject_2_role'", 'null': 'True', 'to': u"orm['core.PedigreeRelationshipRole']"})
        },
        u'core.relation': {
            'Meta': {'object_name': 'Relation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'typ': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '255'})
        },
        u'core.subject': {
            'Meta': {'ordering': "['organization', 'organization_subject_id']", 'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('core.encryption.encryptionFields.EncryptDateField', [], {'max_length': '40'}),
            'first_name': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '136'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '168'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Organization']"}),
            'organization_subject_id': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '264'})
        },
        u'core.subjectgroup': {
            'Meta': {'ordering': "['group']", 'object_name': 'SubjectGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Subject']", 'symmetrical': 'False'})
        },
        u'core.subjectvalidation': {
            'Meta': {'object_name': 'SubjectValidation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Organization']"}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['core']