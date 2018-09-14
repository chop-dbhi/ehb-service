# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.encryption.encryptionFields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('path', models.CharField(max_length=255, verbose_name=b'Path to record collection', blank=True)),
                ('record_id', models.CharField(max_length=50, verbose_name=b'Record ID in External System')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalRecordGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('external_records', models.ManyToManyField(to='core.ExternalRecord')),
            ],
            options={
                'ordering': ['group'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalRecordLabel',
            fields=[
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=100, verbose_name=b'Label')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalRecordRelation',
            fields=[
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('external_record', models.ForeignKey(related_name='external_record', default=None, to='core.ExternalRecord', null=True)),
                ('related_record', models.ForeignKey(related_name='related_record', default=None, to='core.ExternalRecord', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('name', models.CharField(unique=True, max_length=200, verbose_name=b'External System Name')),
                ('url', models.URLField(unique=True, max_length=255, verbose_name=b'External System URL')),
                ('description', models.TextField(help_text=b'Please briefly describe this external system.', verbose_name=b'System Description')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('name', core.encryption.encryptionFields.EncryptCharField(unique=True, max_length=255, verbose_name=b'Group Name')),
                ('client_key', models.CharField(max_length=255, verbose_name=b'Client KEY')),
                ('is_locking', models.BooleanField(default=False, verbose_name=b'Lock Group')),
                ('description', models.TextField(help_text=b'Please briefly describe this Group.', verbose_name=b'Group Description')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupEhbKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('key', core.encryption.encryptionFields.EncryptCharField(verbose_name=b'EHB KEY', unique=True, max_length=255, editable=False, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name=b'Remote Host IP Address')),
                ('host_name', models.CharField(default=b'', max_length=255, verbose_name=b'Name', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('subject_id_label', models.CharField(default=b'Record ID', max_length=50, verbose_name=b'Unique Subject Record ID Label')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PedigreeSubjectRelation',
            fields=[
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('protocol_id', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('typ', models.CharField(default=b'Label', max_length=255, verbose_name=b'Relation Type', choices=[(b'generic', b'Generic'), (b'label', b'Label'), (b'file', b'File'), (b'familial-parent', b'Familial-Parent'), (b'familial-child', b'Familial-Child'), (b'familial-sibling', b'Familial-Sibling'), (b'familial-half-sibling', b'Familial-half-Sibling'), (b'diagnosis', b'Diagnosis')])),
                ('desc', models.CharField(max_length=255, null=True, verbose_name=b'Descriptor', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('first_name', core.encryption.encryptionFields.EncryptCharField(max_length=255, verbose_name=b'First Name')),
                ('last_name', core.encryption.encryptionFields.EncryptCharField(max_length=255, verbose_name=b'Last Name')),
                ('organization_subject_id', core.encryption.encryptionFields.EncryptCharField(max_length=255, verbose_name=b'Organization Subject Record ID')),
                ('dob', core.encryption.encryptionFields.EncryptDateField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', max_length=10, verbose_name=b'Date Of Birth')),
                ('organization', models.ForeignKey(to='core.Organization')),
            ],
            options={
                'ordering': ['organization', 'organization_subject_id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Creation DateTime', auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime')),
                ('group', models.ForeignKey(to='core.Group', unique=True)),
                ('subjects', models.ManyToManyField(to='core.Subject')),
            ],
            options={
                'ordering': ['group'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectValidation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('regex', models.CharField(max_length=70)),
                ('organization', models.ForeignKey(to='core.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pedigreesubjectrelation',
            name='subject_1',
            field=models.ForeignKey(related_name='subject_1', default=None, to='core.Subject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pedigreesubjectrelation',
            name='subject_1_role',
            field=models.ForeignKey(related_name='subject_1_role', default=None, to='core.Relation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pedigreesubjectrelation',
            name='subject_2',
            field=models.ForeignKey(related_name='subject_2', default=None, to='core.Subject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pedigreesubjectrelation',
            name='subject_2_role',
            field=models.ForeignKey(related_name='subject_2_role', default=None, to='core.Relation', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='machineclient',
            unique_together=set([('ip_address', 'host_name')]),
        ),
        migrations.AddField(
            model_name='group',
            name='ehb_key',
            field=models.ForeignKey(blank=True, editable=False, to='core.GroupEhbKey', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalsystem',
            name='subjects',
            field=models.ManyToManyField(to='core.Subject', through='core.ExternalRecord', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalrecordrelation',
            name='relation_type',
            field=models.ForeignKey(to='core.Relation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalrecordgroup',
            name='group',
            field=models.ForeignKey(to='core.Group', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalrecord',
            name='external_system',
            field=models.ForeignKey(verbose_name=b'External System', to='core.ExternalSystem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalrecord',
            name='label',
            field=models.ForeignKey(default=1, verbose_name=b'Label', to='core.ExternalRecordLabel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalrecord',
            name='subject',
            field=models.ForeignKey(to='core.Subject'),
            preserve_default=True,
        ),
    ]
