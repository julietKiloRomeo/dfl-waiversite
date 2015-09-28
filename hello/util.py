# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:12:42 2015

@author: jkr
"""

import requests
from bs4 import BeautifulSoup as bs
import re
from models import Player, Team
from django.contrib.auth.models import User

def latest_trades():
    trade1 = 'Wes Welker'
    trade2 = 'Pat Montgomery'
    trade3 = 'Dan Marino'
    
    return [trade1, trade2, trade3]
    
def url_rows(url):
    r = requests.get(url)
    page = r.content
    soup = bs(page, 'html.parser')
    rows = soup.find_all('tr', {"class": re.compile("^player")})
    return rows

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

    m = re.search('([A-Z]{2,4}) ?-? ?([A-Z]{2,5})?', pos_team)
    if m:
        pos     = m.group(1)
        team    = m.group(2)

    return{'name':name, 'pos':pos, 'team':team, 'id':ID, 'owner':(owner_url, owner_name)}        


def scrapeteam(id):
    url = 'http://fantasy.nfl.com/league/395388/team/%.0f' % id
    rows = url_rows(url)
    
    players = []    
    for r in rows:        
        links   = r.find_all('a', {"class": re.compile("^playerCard")}  )
        name    = links[0].contents[0]
        ID_txt  = links[0].get('href')
        
        m = re.search('playerId=([0-9]{2,12})', ID_txt)
        if m:
            ID = m.group(1)
        else:
            ID = None
            
        players.append( (name, ID) )
    
    return players

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


def bid_winner(bids):
    sorted_bids = sorted(bids, key=lambda x:x[0], reverse=True)
    for b in sorted_bids:
        # b = [dollars, bid]
        # bid has fields team, amount, (player to-)drop, player
        players_on_team = Player.objects.filter(dflteam = b[1].team)

        has_money = b[1].team.account >= b[0]
        can_drop  = b[1].player in players_on_team
        if has_money and can_drop:
            return b[1]
