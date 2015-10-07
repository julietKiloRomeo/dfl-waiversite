# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_team_avatar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Greeting',
        ),
        migrations.AddField(
            model_name='player',
            name='league_pos',
            field=models.IntegerField(default=0),
        ),
    ]
