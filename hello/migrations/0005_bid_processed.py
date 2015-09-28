# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_auto_20150922_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
