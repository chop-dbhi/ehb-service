# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'core_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('subject_id_label', self.gf('django.db.models.fields.CharField')(default='Record ID', max_length=50)),
        ))
        db.send_create_signal(u'core', ['Organization'])

        # Adding model 'Subject'
        db.create_table(u'core_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('first_name', self.gf('core.encryption.encryptionFields.EncryptCharField')(max_length=136)),
            ('last_name', self.gf('core.encryption.encryptionFields.EncryptCharField')(max_length=168)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Organization'])),
            ('organization_subject_id', self.gf('core.encryption.encryptionFields.EncryptCharField')(max_length=264)),
            ('dob', self.gf('core.encryption.encryptionFields.EncryptDateField')(max_length=40)),
        ))
        db.send_create_signal(u'core', ['Subject'])

        # Adding model 'GroupEhbKey'
        db.create_table(u'core_groupehbkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('key', self.gf('core.encryption.encryptionFields.EncryptCharField')(unique=True, max_length=232, blank=True)),
        ))
        db.send_create_signal(u'core', ['GroupEhbKey'])

        # Adding model 'Group'
        db.create_table(u'core_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('name', self.gf('core.encryption.encryptionFields.EncryptCharField')(unique=True, max_length=232)),
            ('client_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_locking', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ehb_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.GroupEhbKey'], unique=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Group'])

        # Adding model 'SubjectGroup'
        db.create_table(u'core_subjectgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Group'], unique=True)),
        ))
        db.send_create_signal(u'core', ['SubjectGroup'])

        # Adding M2M table for field subjects on 'SubjectGroup'
        m2m_table_name = db.shorten_name(u'core_subjectgroup_subjects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subjectgroup', models.ForeignKey(orm[u'core.subjectgroup'], null=False)),
            ('subject', models.ForeignKey(orm[u'core.subject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subjectgroup_id', 'subject_id'])

        # Adding model 'ExternalRecordRelation'
        db.create_table(u'core_externalrecordrelation', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'core', ['ExternalRecordRelation'])

        # Adding model 'ExternalSystem'
        db.create_table(u'core_externalsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['ExternalSystem'])

        # Adding model 'ExternalRecord'
        db.create_table(u'core_externalrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('external_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ExternalSystem'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('record_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('relation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ExternalRecordRelation'])),
        ))
        db.send_create_signal(u'core', ['ExternalRecord'])

        # Adding model 'ExternalRecordGroup'
        db.create_table(u'core_externalrecordgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Group'], unique=True)),
        ))
        db.send_create_signal(u'core', ['ExternalRecordGroup'])

        # Adding M2M table for field external_records on 'ExternalRecordGroup'
        m2m_table_name = db.shorten_name(u'core_externalrecordgroup_external_records')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('externalrecordgroup', models.ForeignKey(orm[u'core.externalrecordgroup'], null=False)),
            ('externalrecord', models.ForeignKey(orm[u'core.externalrecord'], null=False))
        ))
        db.create_unique(m2m_table_name, ['externalrecordgroup_id', 'externalrecord_id'])

        # Adding model 'MachineClient'
        db.create_table(u'core_machineclient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('host_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['MachineClient'])

        # Adding unique constraint on 'MachineClient', fields ['ip_address', 'host_name']
        db.create_unique(u'core_machineclient', ['ip_address', 'host_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'MachineClient', fields ['ip_address', 'host_name']
        db.delete_unique(u'core_machineclient', ['ip_address', 'host_name'])

        # Deleting model 'Organization'
        db.delete_table(u'core_organization')

        # Deleting model 'Subject'
        db.delete_table(u'core_subject')

        # Deleting model 'GroupEhbKey'
        db.delete_table(u'core_groupehbkey')

        # Deleting model 'Group'
        db.delete_table(u'core_group')

        # Deleting model 'SubjectGroup'
        db.delete_table(u'core_subjectgroup')

        # Removing M2M table for field subjects on 'SubjectGroup'
        db.delete_table(db.shorten_name(u'core_subjectgroup_subjects'))

        # Deleting model 'ExternalRecordRelation'
        db.delete_table(u'core_externalrecordrelation')

        # Deleting model 'ExternalSystem'
        db.delete_table(u'core_externalsystem')

        # Deleting model 'ExternalRecord'
        db.delete_table(u'core_externalrecord')

        # Deleting model 'ExternalRecordGroup'
        db.delete_table(u'core_externalrecordgroup')

        # Removing M2M table for field external_records on 'ExternalRecordGroup'
        db.delete_table(db.shorten_name(u'core_externalrecordgroup_external_records'))

        # Deleting model 'MachineClient'
        db.delete_table(u'core_machineclient')


    models = {
        u'core.externalrecord': {
            'Meta': {'object_name': 'ExternalRecord'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ExternalSystem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'record_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ExternalRecordRelation']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"})
        },
        u'core.externalrecordgroup': {
            'Meta': {'ordering': "['group']", 'object_name': 'ExternalRecordGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_records': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.ExternalRecord']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.externalrecordrelation': {
            'Meta': {'ordering': "['id']", 'object_name': 'ExternalRecordRelation'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.externalsystem': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExternalSystem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('core.encryption.encryptionFields.EncryptCharField', [], {'unique': 'True', 'max_length': '232'})
        },
        u'core.groupehbkey': {
            'Meta': {'object_name': 'GroupEhbKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('core.encryption.encryptionFields.EncryptCharField', [], {'unique': 'True', 'max_length': '232', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.machineclient': {
            'Meta': {'unique_together': "(('ip_address', 'host_name'),)", 'object_name': 'MachineClient'},
            'host_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'core.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'subject_id_label': ('django.db.models.fields.CharField', [], {'default': "'Record ID'", 'max_length': '50'})
        },
        u'core.subject': {
            'Meta': {'ordering': "['organization', 'organization_subject_id']", 'object_name': 'Subject'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('core.encryption.encryptionFields.EncryptDateField', [], {'max_length': '40'}),
            'first_name': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '136'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '168'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Organization']"}),
            'organization_subject_id': ('core.encryption.encryptionFields.EncryptCharField', [], {'max_length': '264'})
        },
        u'core.subjectgroup': {
            'Meta': {'ordering': "['group']", 'object_name': 'SubjectGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Subject']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['core']
