# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', 'django17Generated_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalrecord',
            name='label',
            field=models.ForeignKey(default=1, verbose_name=b'Label', to='core.ExternalRecordLabel', null=True),
            preserve_default=True,
        ),
    ]
