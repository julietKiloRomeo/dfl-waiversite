# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_bid_drop'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='succesful',
            field=models.BooleanField(default=False),
        ),
    ]
