from django.test import TestCase

from hello.models import Team, Player, Bid
from django.contrib.auth.models import User
from hello import util
from django.test import Client


import datetime
from django.utils import timezone







class AuctionTestCase(TestCase):
    def setUp(self):
        
        users   = []        
        teams   = []        
        players = []        
        
        users.append(User.objects.create(username='alpha', password='asd'))
        users.append(User.objects.create(username='beta', password='asd'))
        users.append(User.objects.create(username='gamma', password='asd'))
        
        teams.append(Team.objects.create(name="a", account=150, owner = users[0], nfl_id= 1 , league_pos = 1))
        teams.append(Team.objects.create(name="b", account=150, owner = users[1], nfl_id= 2 , league_pos = 2))
        teams.append(Team.objects.create(name="c", account=150, owner = users[2], nfl_id= 3 , league_pos = 3))

        players.append(Player.objects.create(name='rb1', nflteam='Saints', dflteam = None,     nfl_id=1))
        players.append(Player.objects.create(name='rb2', nflteam='Saints', dflteam = teams[0], nfl_id=2))
        players.append(Player.objects.create(name='rb3', nflteam='Saints', dflteam = teams[1], nfl_id=3))
        players.append(Player.objects.create(name='rb4', nflteam='Saints', dflteam = teams[2], nfl_id=4))

        players.append(Player.objects.create(name='wr1', nflteam='Saints', dflteam = None,     nfl_id=5))
        players.append(Player.objects.create(name='wr2', nflteam='Saints', dflteam = teams[0], nfl_id=6))
        players.append(Player.objects.create(name='wr3', nflteam='Saints', dflteam = teams[1], nfl_id=7))
        players.append(Player.objects.create(name='wr4', nflteam='Saints', dflteam = teams[2], nfl_id=8))

        players.append(Player.objects.create(name='rb5', nflteam='Saints', dflteam = None,     nfl_id=9))

        Bid.objects.create(        team     = teams[0], 
                                   amount   = 100, 
                                   priority = 1, 
                                   player   = players[0], 
                                   drop     = Player.objects.get(name='rb2'))

        Bid.objects.create(        team     = teams[1], 
                                   amount   = 101, 
                                   priority = 1, 
                                   player   = players[0], 
                                   drop     = Player.objects.get(name='rb3'))


        Bid.objects.create(        team     = teams[0], 
                                   amount   = 100, 
                                   priority = 2, 
                                   player   = players[4], 
                                   drop     = Player.objects.get(name='wr2'))

        Bid.objects.create(        team     = teams[1], 
                                   amount   = 101, 
                                   priority = 2, 
                                   player   = players[4], 
                                   drop     = Player.objects.get(name='wr3'))


        Bid.objects.create(        team     = teams[1], 
                                   amount   = 2, 
                                   priority = 3, 
                                   player   = players[8], 
                                   drop     = Player.objects.get(name='rb3'))

        Bid.objects.create(        team     = teams[2], 
                                   amount   = 1, 
                                   priority = 3, 
                                   player   = players[8], 
                                   drop     = Player.objects.get(name='rb4'))

        Bid.objects.create(        team     = teams[1], 
                                   amount   = 1, 
                                   priority = 3, 
                                   player   = players[8], 
                                   drop     = Player.objects.get(name='wr3'))



    def test_auctions(self):
        """Test several auction scenarios"""
        results, droplist = util.round_results(commit=False)

        print 'Test without commiting'
        
        drop1 = Player.objects.get(name='rb3')
        drop2 = Player.objects.get(name='wr2')

        for p in results.keys():
            print p.name
            for b in results[p]['bids']:
                print b
            if isinstance(results[p]['winner'], basestring):
                print 'Won by %s\n' % results[p]['winner']
            else:
                print 'Won by %s\n' % results[p]['winner'].team.name

        self.assertEqual(droplist[0], drop1.pk)
        self.assertEqual(droplist[1], drop2.pk)

        print 'Check accounts'
        teams = Team.objects.all()
        for t in teams:
            print '%s : %d' % (t.name, t.account)
            self.assertEqual(t.account, 150)
            
    def test_auctions_commit(self):
        results, droplist = util.round_results(commit=True)

        print 'Test with commiting'

        drop1 = Player.objects.get(name='rb3')
        drop2 = Player.objects.get(name='wr2')

        for p in results.keys():
            print p.name
            for b in results[p]['bids']:
                print b
            if isinstance(results[p]['winner'], basestring):
                print 'Won by %s\n' % results[p]['winner']
            else:
                print 'Won by %s\n' % results[p]['winner'].team.name

        self.assertEqual(droplist[0], drop1.pk)
        self.assertEqual(droplist[1], drop2.pk)

        print 'Check accounts'
        teams = Team.objects.all()
        accounts = {'a':50, 'b':49, 'c':149}
        for t in teams:
            print '%s : %d' % (t.name, t.account)
            self.assertEqual(t.account, accounts[t.name])
        self.assertEqual(len(Bid.objects.filter(processed=True)), 7)        

    def test_index(self):
        results, droplist = util.round_results(commit=True)
        client = Client()
        response = client.get('/')
        print response.context['trades']
#        self.assertContains(response, "No polls are available.")
#        self.assertQuerysetEqual(response.context['trades'], [])        
        self.assertEqual(len(response.context['trades']), 0)        
        self.assertEqual(len(Bid.objects.filter(processed=True)), 7)        
        self.assertEqual(len(Bid.objects.filter(succesful=True)), 3)        
        

    def test_timer(self):
        # monday
        t_2_w = datetime.datetime(year=2015, month=11, day=2, hour=14)
        # tuesday
        t_1_w = datetime.datetime(year=2015, month=11, day=3, hour=7)

        t_1_w =  timezone.make_aware(t_1_w, timezone.get_current_timezone())
        t_2_w =  timezone.make_aware(t_2_w, timezone.get_current_timezone())

        self.assertTrue( util.is_1_waiver_period(t = t_1_w) )        
        self.assertTrue( util.is_2_waiver_period(t = t_2_w) )        
        
        # wednesday
        t_2_w = datetime.datetime(year=2015, month=11, day=4, hour=14)
        t_2_w =  timezone.make_aware(t_2_w, timezone.get_current_timezone())
        
        self.assertTrue( util.is_2_waiver_period(t = t_2_w) )        
        

    def test_scrapers(self):
        util.add_from_search('Tom Brady')
        
        brady = Player.objects.get(name__icontains = "brady")        

        self.assertEqual(brady.name, 'Tom Brady')        
        self.assertEqual(brady.position, Player.QB)        

        players, rank = util.scrapeteam(1)

        self.assertTrue(rank < 13 and rank > 0)        
        self.assertTrue(len(players) > 14 )        




        