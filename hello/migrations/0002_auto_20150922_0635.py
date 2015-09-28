# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='dflteam',
            field=models.ForeignKey(to='hello.Team', null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='nflteam',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
