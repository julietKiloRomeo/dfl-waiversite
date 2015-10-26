# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0011_auto_20151007_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='swapped_on_nfl',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='team',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
    ]
