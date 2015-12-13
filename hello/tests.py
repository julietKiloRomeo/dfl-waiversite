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

        print ''
        print '----------------- Test without commit: ------------------------'
        
        drop1 = Player.objects.get(name='rb3')
        drop2 = Player.objects.get(name='wr2')


        print '%40s' % ('Check auction winners:'),
        self.assertEqual(droplist[0], drop1.pk)
        self.assertEqual(droplist[1], drop2.pk)
        print ' OK'

        print '%40s' % ('Check accounts:'),
        teams = Team.objects.all()
        for t in teams:
            self.assertEqual(t.account, 150)
        print ' OK'
            
    def test_auctions_commit(self):
        results, droplist = util.round_results(commit=True)

        print ''
        print '------------------- Test with commit: --------------------------'

        drop1 = Player.objects.get(name='rb3')
        drop2 = Player.objects.get(name='wr2')
        
        print '%40s' % ('Check auction winners:'),
        self.assertEqual(droplist[0], drop1.pk)
        self.assertEqual(droplist[1], drop2.pk)
        print ' OK'

        invalid_drop = Bid.objects.filter(player__name = 'rb5').filter(drop__name = 'rb3')[0]
        invalid_funds = Bid.objects.filter(player__name = 'wr1').filter(drop__name = 'wr3')[0]
                
        print '%40s' % ('Check invalid drop:'),
        self.assertEqual(invalid_drop.validity, Bid.DROP)
        print ' OK'

        print '%40s' % ('Check invalid funds:'),
        self.assertEqual(invalid_funds.validity, Bid.FUNDS)
        print ' OK'

        print '%40s' % ('Check accounts:'),
        teams = Team.objects.all()
        accounts = {'a':50, 'b':49, 'c':149}
        for t in teams:
            self.assertEqual(t.account, accounts[t.name])
        self.assertEqual(len(Bid.objects.filter(processed=True)), 7)        
        print ' OK'

    def test_results_page(self):
        print ''
        print '------------------- Testing results page: --------------------------'
        results, droplist = util.round_results(commit=True)
        this_week         = util.waiver_week(timezone.now())
        url = '/results/%d/' % (this_week)
        client = Client()
        response = client.get(url)

        
        print '%40s' % ('Check wr1 present in html context:'),
        wr1 = Player.objects.get(name='wr1')
        self.assertTrue(wr1 in response.context['rounds'].keys())        
        print ' OK'



    def test_index_page(self):
        print ''
        print '------------------- Testing front page: --------------------------'
        results, droplist = util.round_results(commit=True)
        client = Client()
        response = client.get('/')
#        self.assertContains(response, "No polls are available.")
#        self.assertQuerysetEqual(response.context['trades'], [])        

        print '%40s' % ('Check for trades in html context:'),
        self.assertEqual(len(response.context['trades']), 0)        
        self.assertEqual(len(Bid.objects.filter(processed=True)), 7)        
        self.assertEqual(len(Bid.objects.filter(succesful=True)), 3)        
        print ' OK'
        

    def test_timer(self):
        print ''
        print '------------------- Testing timer functions: --------------------------'
        # monday
        t_2_w = datetime.datetime(year=2015, month=11, day=2, hour=14)
        # tuesday
        t_1_w = datetime.datetime(year=2015, month=11, day=3, hour=7)

        t_1_w =  timezone.make_aware(t_1_w, timezone.get_current_timezone())
        t_2_w =  timezone.make_aware(t_2_w, timezone.get_current_timezone())

        print '%40s' % ('Monday 14:00 is waiver period 2:'),
        self.assertTrue( util.is_2_waiver_period(t = t_2_w) )        
        print ' OK'

        print '%40s' % ('Tuesday 07:00 is waiver period 1:'),
        self.assertTrue( util.is_1_waiver_period(t = t_1_w) )        
        print ' OK'

        # wednesday
        t_2_w = datetime.datetime(year=2015, month=11, day=4, hour=14)
        t_2_w =  timezone.make_aware(t_2_w, timezone.get_current_timezone())
        
        print '%40s' % ('Wednesday 14:00 is waiver period 2:'),
        self.assertTrue( util.is_2_waiver_period(t = t_2_w) )        
        print ' OK'
        
    def test_scrapers(self):
        print ''
        print '------------------- Testing NFL scraper: --------------------------'
        util.add_from_search('Tom Brady')
        
        brady = Player.objects.get(name__icontains = "brady")        

        print '%40s' % ('Scrape Tom Brady from NFL and add to DB:'),
        self.assertEqual(brady.name, 'Tom Brady')        
        self.assertEqual(brady.position, Player.QB)        
        print ' OK'

        print '%40s' % ('Scrape Superheroes and verify:'),
        players, rank = util.scrapeteam(1)

        self.assertTrue(rank < 13 and rank > 0)        
        self.assertTrue(len(players) > 14 )        
        print ' OK'


    def test_nfllogin(self):
        print ''
        print '------------------- Testing NFL login: --------------------------'
        session = util.nfl_login()
        session.login()
        
        print '%40s' % ('Testing that NFL_USER can log in to fantasy.nfl.com:'),
        self.assertTrue(session.is_logged_in())        
        print ' OK'


        