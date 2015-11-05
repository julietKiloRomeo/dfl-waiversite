# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0014_auto_20151102_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='validity',
            field=models.IntegerField(default=0, choices=[(0, b'valid'), (1, b'drop'), (2, b'funds')]),
        ),
    ]
