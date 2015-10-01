# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_bid_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'avatars/', blank=True),
        ),
    ]
