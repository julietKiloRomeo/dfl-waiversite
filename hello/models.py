from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Team(models.Model):
    name    = models.CharField(max_length=100)
    account = models.IntegerField()
    owner   = models.OneToOneField(User)
    nfl_id  = models.IntegerField(unique=True)
    def __unicode__(self):
        return self.name

class Bid(models.Model):
    team    = models.ForeignKey('Team')
    amount  = models.IntegerField()
    player  = models.ForeignKey('Player')
    drop    = models.ForeignKey('Player', related_name='to_drop', null=True)
    date    = models.DateTimeField('date placed', auto_now_add=True)
    processed = models.BooleanField(default=False)
    def __unicode__(self):
        return '%20s : %s' % (self.team.name, self.player.name)
        

class Player(models.Model):
    name        = models.CharField(max_length=100)
    nflteam     = models.CharField(max_length=100, null=True)
    dflteam     = models.ForeignKey('Team', null=True)
    nfl_id      = models.IntegerField(unique=True)
    def __unicode__(self):
        return self.name
    
