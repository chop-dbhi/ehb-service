# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', 'externalRecordLabelDefault'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalrecord',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='externalrecordgroup',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='externalrecordlabel',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='externalrecordrelation',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='externalsystem',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='groupehbkey',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='pedigreesubjectrelation',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='relation',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
        migrations.AlterField(
            model_name='subjectgroup',
            name='modified',
            field=models.DateTimeField(help_text=b'Please use date format: <em>YYYY-MM-DD</em>', verbose_name=b'Record Last Modified DateTime', auto_now=True),
        ),
    ]
