# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20150922_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='nfl_id',
            field=models.IntegerField(unique=True),
        ),
    ]
