# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0013_player_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.IntegerField(default=None, null=True, choices=[(0, b'QB'), (1, b'RB'), (2, b'WR'), (3, b'TE'), (4, b'DEF'), (5, b'K')]),
        ),
    ]
