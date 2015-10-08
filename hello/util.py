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
    w_0 = datetime.datetime(year=2015, month=9, day=16, hour=14)
    w_0 =  timezone.make_aware(w_0, timezone.get_current_timezone())
    return (d-w_0).days//7+1

def latest_trades():
    trades = Bid.objects.filter(succesful=True)
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

def query(name):
    url = 'http://fantasy.nfl.com/league/395388/players/search?searchQuery=%s' % (name)
    rows = url_rows(url)

    results = []
    for r in rows:
        results.append(searchresult_2_player(r))

    return results

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

    return{'name':name, 'pos':pos, 'team':team, 'id':ID, 'owner':(owner_url, owner_name)}        


def scrapeteam(id):
    url = 'http://fantasy.nfl.com/league/395388/team/%.0f' % id
    rows, soup = url_rows(url)
    #        <li class="first"><em>Rank</em> <strong>7</strong></li>
    rank_ul    = soup.find_all('ul', {"class": re.compile("^teamStats")}  )[0]
    rank       = rank_ul.find_all('li', {"class": re.compile("^first")}  )[0].strong.contents[0]

    
    
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
    else:
        ID = None
        
    if ID:
        username = dfl_owner[1]
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
        else:
            u = User.objects.create_user(username, 'asd@gmail.com', 'dfl_is_#1')
        
        team, created = Team.objects.update_or_create(nfl_id = ID,
                                                      defaults ={'name' : dfl_owner[1], 
                                                                 'owner' : u, 
                                                                 'account' : 150})
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
    current_time = datetime.datetime.now()
    
    # get friday, one week ago, at 16 o'clock
    last_wednesday = (current_time.date() -
                      datetime.timedelta(days=current_time.weekday()) + 
                      datetime.timedelta(days=2, weeks=-1))
    
    l_w_at_14 = datetime.datetime.combine(last_wednesday, datetime.time(14))
    return l_w_at_14

def is_2_waiver_period():
    current_time = datetime.datetime.now()
    is_w_after_14 = (current_time.weekday() == 2) and current_time.hour > 14
    is_thursday   = current_time.weekday() == 3
    is_f_after_4  = (current_time.weekday() == 4) and current_time.hour > 4
    
    return is_w_after_14 or is_thursday or is_f_after_4

    


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

def resolve_round(rounds):
    # use divide_bids to create rounds dict
    # go through all rounds
    round_priority  = []
    bids_to_process = []
    for p in rounds.keys():
        is_resolved = rounds[p]['winner']
        if not is_resolved:
            for b in rounds[p]['bids']:
                db_bid = Bid.objects.get(pk=b.pk)
                if db_bid.is_valid():
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

def round_results(commit=False):
    current_bids    = Bid.objects.filter(processed=False)
    rounds          = divide_bids(current_bids)
    
    rounds_left = True
    droplist    = []
    while rounds_left>0:
        rounds, bids_to_process = resolve_round(rounds)
        for b in bids_to_process:
            droplist.append(b)
            b.drop.dflteam = None
            b.drop.save()
            if commit:
                db_team = Team.objects.get(pk=b.team.pk)
                db_bid  = Bid.objects.get(pk=b.pk)
                db_team.account -= b.amount
                db_team.save()
                db_bid.succesful = True
                db_bid.save()

        winner_list = [rnd['winner'] for rnd in rounds.itervalues()  ]
        rounds_left = sum(x is None for x in winner_list)
    if not commit:
        for b in droplist:            
            b.drop.dflteam = b.team
            b.drop.save()
    else:
        Bid.objects.all().update(processed=True)
        
    return (rounds, droplist)
        