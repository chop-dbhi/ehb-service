# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='ehb_key',
            field=models.ForeignKey(blank=True, editable=False, to='core.GroupEhbKey', unique=True),
        ),
    ]
