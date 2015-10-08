from django.shortcuts import render
#from django.http import HttpResponse
from django.http import HttpResponseRedirect
import util
from django.contrib import auth
from models import Player, Team, Bid
from django.conf import settings

def index(request):
    trades = util.latest_trades()
    N_bids = len(Bid.objects.filter(processed=False))
    teams = Team.objects.all()
    return render(request, 'index.html', {'trades': trades, 'N':N_bids, 'teams':teams})

def delete_bid(request, bid_id):
    u       = request.user
    bid = Bid.objects.get(pk=bid_id)
    if u.is_authenticated():
        if bid.team.owner==u:
            bid.delete()
        return HttpResponseRedirect("/team")
    else:
        return HttpResponseRedirect("/login")
    
def bid(request, nfl_id):
    u       = request.user
    if u.is_authenticated():
        if not settings.LOCK_BIDS:
            p       = Player.objects.get(nfl_id=nfl_id)
            team    = Team.objects.get(owner=u)
            roster  = Player.objects.filter(dflteam=team)
            if request.method == 'POST':
                val         = int(request.POST.get('bidvalue'))
                pk_to_drop  = request.POST.get('Drop')
                dropee      = Player.objects.get(pk=pk_to_drop)
                priority    = request.POST.get('Priority')
                b           = Bid(team=team, amount=val, player=p, drop=dropee, priority=priority)
                b.save()
                return HttpResponseRedirect("/team")
            else:
                return render(request, 'bid.html', {'player': p, 'roster':roster})
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def team(request, team_id=None):
    u       = request.user
    if team_id:
        team    = Team.objects.get(nfl_id=team_id)
    else:
        team    = Team.objects.get(owner=u)
    is_user_home = False
    if u.is_authenticated():
        if team.owner==u:
            bids    = Bid.objects.filter(team=team).filter(processed=False)
            is_user_home = True
        else:
            bids = None
        roster  = Player.objects.filter(dflteam=team)
        return render(request, 'team.html', {'user': request.user, 
                                             'team':team, 
                                             'bids':bids, 
                                             'is_user_home':is_user_home, 
                                             'roster':roster})
    else:
        return HttpResponseRedirect("/login")
    
def search(request):
    u       = request.user
    if u.is_authenticated():
        if request.method == 'POST':
            if 'Search_NFL' in request.POST:        
                util.add_from_search(request.POST.get('playername'))
            matches = Player.objects.filter(name__icontains = request.POST.get('playername'))
        else:
            matches = []
    
        return render(request, 'search.html', {'matches': matches})
    else:
        return HttpResponseRedirect("/login")

def rules(request):
    return render(request, 'rules.html')

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
    return HttpResponseRedirect("/")
        
def week_results(request):
    u       = request.user
    if settings.SHOW_RESULTS or (u.is_staff and settings.SHOW_RESULTS_FOR_STAFF) or (u.is_superuser and settings.SHOW_RESULTS_FOR_SU):
        current_bids        = Bid.objects.filter(processed=False)
        rounds = util.divide_bids(current_bids)
        
        rounds_left = True
        droplist    = []
        while rounds_left>0:
            rounds, bids_to_process = util.resolve_round(rounds)
            for b in bids_to_process:
                droplist.append(b)
                t = b.team
#                t.account -= b.amount
                t.drop(b.drop)
            winner_list = [rnd['winner'] for rnd in rounds.itervalues()  ]
            rounds_left = sum(x is None for x in winner_list)
        for b in droplist:
            b.drop.dfl_team = b.team
            b.drop.save()
        return render(request, 'results.html', {'rounds':rounds})
    else:
        return HttpResponseRedirect("/")
        
    