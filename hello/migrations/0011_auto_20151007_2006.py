# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0010_auto_20151007_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='league_pos',
        ),
        migrations.AddField(
            model_name='team',
            name='league_pos',
            field=models.IntegerField(default=0),
        ),
    ]
