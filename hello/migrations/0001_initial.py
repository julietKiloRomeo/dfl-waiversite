# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'date placed')),
            ],
        ),
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('nflteam', models.CharField(max_length=100)),
                ('nfl_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('account', models.IntegerField()),
                ('nfl_id', models.IntegerField()),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='dflteam',
            field=models.ForeignKey(to='hello.Team'),
        ),
        migrations.AddField(
            model_name='bid',
            name='player',
            field=models.ForeignKey(to='hello.Player'),
        ),
        migrations.AddField(
            model_name='bid',
            name='team',
            field=models.ForeignKey(to='hello.Team'),
        ),
    ]
