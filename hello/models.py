from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Team(models.Model):
    name    = models.CharField(max_length=100)
    account = models.IntegerField()
    owner   = models.ForeignKey(User, unique=True)

class Bid(models.Model):
    team    = models.ForeignKey('Team')
    amount  = models.IntegerField()
    player  = models.ForeignKey('Player')
    date    = models.DateTimeField('date placed', auto_now_add=True)

class Player(models.Model):
    name        = models.CharField()
    nflteam     = models.CharField()
    dflteam     = models.ForeignKey('Team')
    