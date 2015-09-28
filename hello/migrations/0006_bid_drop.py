# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_bid_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='drop',
            field=models.ForeignKey(related_name='to_drop', to='hello.Player', null=True),
        ),
    ]
