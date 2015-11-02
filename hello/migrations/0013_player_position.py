# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0012_auto_20151026_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.IntegerField(default=2, choices=[(0, b'QB'), (1, b'RB'), (2, b'WR'), (3, b'TE'), (4, b'DEF'), (5, b'K')]),
        ),
    ]
