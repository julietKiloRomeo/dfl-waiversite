# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:12:42 2015

@author: jkr
"""

import requests
from bs4 import BeautifulSoup as bs
import re
from models import Player, Team, Bid
from django.contrib.auth.models import User
import time
import datetime
from django.utils import timezone

def waiver_week(d):
    w_0 = datetime.datetime(year=2015, month=9, day=9, hour=14)
    w_0 =  timezone.make_aware(w_0, timezone.get_current_timezone())
    return (d-w_0).days//7+1

def latest_trades():
    trades = Bid.objects.filter(succesful=True).order_by('team__name', '-amount')
    latest = []
    this_week = waiver_week(timezone.now())
    for t in trades:
        if this_week - waiver_week(t.date) == 1:
            latest.append(t)
    return latest
    
def url_rows(url):
    r = requests.get(url)
    page = r.content
    soup = bs(page, 'html.parser')
    rows = soup.find_all('tr', {"class": re.compile("^player")})
    return (rows, soup)

def searchresult_2_player(row):
    tmp     = row.find_all('td')
    info    = tmp[1] 

    links   = info.find_all('a')
    e       = info.find_all('em')
    ID_txt      = links[0].get('href')
    name        = links[0].contents[0]
    pos_team    = e[0].contents[0]
    
    owner_data = row.find_all('td', {"class":"playerOwner"})[0]
    if len(owner_data.find_all('a')):
        owner_url   = owner_data.a.get('href')
        owner_name  = owner_data.a.contents[0]
    else:
        owner_url   = ''
        owner_name  = ''
    
    m = re.search('playerId=([0-9]{2,12})', ID_txt)
    if m:
        ID = m.group(1)

    m = re.search('([A-Z]{1,4}) ?-? ?([A-Z]{2,5})?', pos_team)
    if m:
        pos     = m.group(1)
        team    = m.group(2)

    return {'name':name, 'pos':pos, 'team':team, 'id':ID, 'owner':(owner_url, owner_name)}        

def query(name):
    url = 'http://fantasy.nfl.com/league/395388/players/search?searchQuery=%s' % (name)
    rows, soup = url_rows(url)

    results = []
    for r in rows:
        results.append(searchresult_2_player(r))

    return results


def scrapeteam(id):
    url        = 'http://fantasy.nfl.com/league/395388/team/%.0f' % id
    rows, soup = url_rows(url)
    #        <span class="teamRank teamId-3">(8)</span>
#    rank_ul    = soup.find_all('span', {"class": re.compile("^teamRank teamId")}  )[0]
#    rank       = rank_ul.find_all('li', {"class": re.compile("^first")}  )[0].strong.contents[0]
    rank       = soup.find_all('span', {"class": re.compile("^teamRank")}  )[0].contents[0][1:-1]


    
    
    players = []    
    for r in rows:        
        links   = r.find_all('a', {"class": re.compile("^playerCard")}  )
        if links:
            name    = links[0].contents[0]
            ID_txt  = links[0].get('href')
            ems     = r.find_all('em')
            
            m = re.search('playerId=([0-9]{2,12})', ID_txt)
            if m:
                ID = m.group(1)
            else:
                ID = None
            m = re.search('- *([A-Z]{1,5})', ems[0].contents[0])
            if m:
                team = m.group(1)
            else:
                team = None
                
            players.append( (name, ID,team) )
    
    return (players, int(rank))

def add_player(p):
    dfl_owner = p['owner']
    m = re.search('team/([0-9]{1,2})', dfl_owner[0])
    if m:
        ID = int(m.group(1))
        team = Team.objects.get(nfl_id=ID)
    else:
        team = None
        
    Player.objects.update_or_create(nfl_id   = p['id'],
                           defaults={ 'name' : p['name'], 
                           'nflteam' : p['team'],
                           'dflteam' : team} )

def add_from_search(q):
    results = query(q)
    for p in results:
        add_player(p)


def update_league():
    for team in Team.objects.all():
        print team
        # delete previous roster
        Player.objects.filter(dflteam=team).update(dflteam=None)
        # get current roster
        players, rank = scrapeteam(team.nfl_id)
        time.sleep(1)
        team.league_position = rank
        team.save()
        for p in players:        
            Player.objects.update_or_create(nfl_id   = int(p[1]),
                                   defaults={ 'name' : p[0], 
                                   'nflteam' : p[2],
                                   'dflteam' : team} )

def last_wednesday_at_14():
    current_time            = timezone.localtime(timezone.now())
    go_back_one_week        = current_time.weekday() <= 2
    monday_of_current_week  = current_time.date() - datetime.timedelta(days=current_time.weekday())
    # get last wednesday. If it is mon, tue or wed it is last week, otherwise wed this week
    last_wednesday = (monday_of_current_week + 
                      datetime.timedelta(days=2, weeks = -1*go_back_one_week  ))
    
    l_w_at_14 = datetime.datetime.combine(last_wednesday, datetime.time(14))
    l_w_at_14 =  timezone.make_aware(l_w_at_14, timezone.get_current_timezone())
    return l_w_at_14

def time_until_open():
    current_time        = timezone.localtime(timezone.now())
    add_two_weeks       = current_time.weekday() <= 2
    next_tuesday_at_06  = last_wednesday_at_14() + datetime.timedelta(weeks=1 + 1*add_two_weeks, days=-1, hours=-8)
    return next_tuesday_at_06 - timezone.now()

def is_1_waiver_period():
    current_time            = timezone.localtime(timezone.now())
    is_tuesday_after_06     = current_time.weekday() == 1 and current_time.hour >= 6
    is_w_before_14          = (current_time.weekday() == 2) and current_time.hour < 14
    
    return is_tuesday_after_06 or is_w_before_14

def is_2_waiver_period():    
    return not is_1_waiver_period()

def clear_all_bids():
    for b in Bid.objects.all():
        # delete previous roster
        b.delete()

def divide_bids(bids):
    # bids should be a list
    rounds = {}
    for b in bids:
        player = b.player
        rounds.setdefault(player, {'winner':None, 'bids':[], 'nonvalid':[]})['bids'].append(b)
    # sort 
    for p in rounds.keys():
        tmp = rounds[p]['bids']
        tmp = sorted(rounds[p]['bids'], key=lambda b: b.frac_amount(), reverse=True) 
        rounds[p]['bids'] = tmp
    
    return rounds

def resolve_round(rounds, droplist):
    # use divide_bids to create rounds dict
    # go through all rounds
    round_priority  = []
    bids_to_process = []
    for p in rounds.keys():
        is_resolved = rounds[p]['winner']
        if not is_resolved:
            for b in rounds[p]['bids']:
                db_bid = Bid.objects.get(pk=b.pk)
                if not db_bid.drop.pk in droplist:
                    round_priority.append( b )
                    break
                else:
                    rounds[p]['nonvalid'].append(b.pk)
            if not round_priority:
                rounds[p]['winner'] = 'None valid'
    round_priority  = sorted(round_priority, key=lambda b: b.priority)
    if round_priority:
        prio_to_resolve = round_priority[0].priority
        while len(round_priority) and round_priority[0].priority == prio_to_resolve:
            winning_bid    = round_priority.pop(0)
            rounds[winning_bid.player]['winner'] = winning_bid
            bids_to_process.append(winning_bid)
    return (rounds, bids_to_process)

def round_results(commit=False, week=None):
    # called with week=None process all unprocessed bids
    # otherwise calculate round results for given week
    if week:
        all_bids        = Bid.objects.filter(processed=True)
        current_bids=[]
        for b in all_bids:
            if waiver_week(b.date)==week:
                current_bids.append(b)
    else:
        current_bids    = Bid.objects.filter(processed=False)

    rounds          = divide_bids(current_bids)
    
    rounds_left = True
    droplist    = []
    while rounds_left>0:
        rounds, bids_to_process = resolve_round(rounds, droplist)
        for b in bids_to_process:
            droplist.append(b.drop.pk)
            if commit:
                db_team = Team.objects.get(pk=b.team.pk)
                db_bid  = Bid.objects.get(pk=b.pk)
                db_team.account -= b.amount
                db_team.save()
                db_bid.succesful = True
                db_bid.save()

        winner_list = [rnd['winner'] for rnd in rounds.itervalues()  ]
        rounds_left = sum(x is None for x in winner_list)
    if commit:
        Bid.objects.all().update(processed=True)
        
    return (rounds, droplist)
        
        
class nfl_login():
    login_url       = 'https://id2.s.nfl.com/fans/login?returnTo=http://www.nfl.com/fantasyfootball'
    league_url      = 'http://fantasy.nfl.com/league/395388'
    management_url  = 'http://fantasy.nfl.com/league/395388/manage'
    addplayer_url   = 'http://fantasy.nfl.com/league/395388/manage/teamrosteraddplayerconfirm'

    def __init__(self):
        self.session = requests.session()
    def login(self):
        payload = {'username': 'jimmy.kjaersgaard@gmail.com', 
                   'password': 'eskadron',
                   'cookiePersisted':'on',
                   'succesUrl':'',
                   's':'',
                   'modal':'1'}
        # do login
        self.session.post(self.login_url, data=payload)

    def is_logged_in(self):
        # if Tommy, Thomas or I am logged in and has permission, management page will display properly
        r = self.session.get(self.management_url)
        m = re.search('League Management', r.content)
        return m is not None
            
    # this has to be called shortly after add/drop or someone else may have performed a transaction - the function looks for the latest message
    def add_drop_succes(self, payload):
        # load frontpage of league
        r       = self.session.get(self.league_url)
        # look for latest add/drop message and parse out (team, add, drop)
        pattern = 'class="teamName teamId-(?P<team>[0-9]*)">.*?added.*?leagueId=395388&playerId=(?P<add>[0-9]*).*?and dropped.*?playerId=(?P<drop>[0-9]*)'
        m       = re.findall(pattern, r.content)
        # do they match the attempted transaction?    
        return m[0][0]==payload['teamId'] and m[0][1]==payload['addPlayerId'] and m[0][2]==payload['dropPlayerId']
        
    def add_drop(self, team, to_add, to_drop):
        payload = {'teamId':team,
                   'addPlayerId':to_add,
                   'dropPlayerId':to_drop,
                   'jSubmit':'Submit'}
        self.session.post(self.addplayer_url, data=payload)
        return self.add_drop_succes(payload)
