# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_bid_succesful'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
