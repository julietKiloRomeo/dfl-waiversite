from django.db import models
from django.contrib.auth.models import User
        
class Bid(models.Model):
    team        = models.ForeignKey('Team')
    amount      = models.IntegerField()
    priority    = models.IntegerField(default=1)
    player      = models.ForeignKey('Player')
    drop        = models.ForeignKey('Player', related_name='to_drop', null=True)
    date        = models.DateTimeField('date placed', auto_now_add=True)
    processed   = models.BooleanField(default=False)
    succesful   = models.BooleanField(default=False)
    swapped_on_nfl   = models.BooleanField(default=False)
    def __unicode__(self):
        s = '%20s %d$ : %s for %s (%.0f)' % (self.team.name, self.amount, self.player.name, self.drop.name, self.priority)
        if self.succesful:
            s += '      WINNER'
        if self.swapped_on_nfl:
            s += ' WAS PROCESSED'
        return s
    def is_valid(self):
        return (self.amount <= self.team.account) and (self.drop.dflteam == self.team)         
    def frac_amount(self):
        # break ties
        return self.amount + self.team.account/151.0/10 + self.team.league_pos/13.0/100

class Player(models.Model):    
    QB  = 0    
    RB  = 1    
    WR  = 2    
    TE  = 3    
    DEF = 4    
    K   = 5    
    POSITIONS = ((QB , 'QB'),
                 (RB , 'RB'),
                 (WR , 'WR'),
                 (TE , 'TE'),
                 (DEF, 'DEF'),
                 (K  , 'K') )

    
    name        = models.CharField(max_length=100)
    nflteam     = models.CharField(max_length=100, null=True)
    dflteam     = models.ForeignKey('Team', null=True)
    nfl_id      = models.IntegerField(unique=True)
    position    = models.IntegerField(choices = POSITIONS, null=True, default = None)
    def __unicode__(self):
        if self.dflteam:
            return '%20s (%s)' % (self.name, self.dflteam.name)
        else:    
            return '%20s ' % (self.name)
            
    def pos_and_name(self):
        return '%-5s  %s' % (self.POSITIONS[self.position][1], self.name)

class Team(models.Model):
    name    = models.CharField(max_length=100)
    account = models.IntegerField()
    owner   = models.OneToOneField(User)
    nfl_id  = models.IntegerField(unique=True)
    # upload_to = "f"  will upload img.jpg to MEDIA_ROOT/f/img.jpg
    avatar  = models.ImageField(upload_to="", blank=True, null=True)
    league_pos  = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name
    def drop(self, player):
        if player.dflteam==self:
            player.dflteam = None
            player.save()


