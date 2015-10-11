from django.shortcuts import render
from django.http import HttpResponseRedirect
import util
from django.contrib import auth
from models import Player, Team, Bid
from django.conf import settings
from django.utils import timezone

def index(request):
    trades = util.latest_trades()
    N_bids = len(Bid.objects.filter(processed=False))
    teams = Team.objects.all().order_by('name')
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
    u           = request.user
    allow_bids  = u.is_authenticated() and (not settings.LOCK_BIDS) and util.is_1_waiver_period()
    if allow_bids:
        p               = Player.objects.get(nfl_id=nfl_id)
        team            = Team.objects.get(owner=u)
        roster          = Player.objects.filter(dflteam=team)
        if request.method == 'POST':
            val         = int(request.POST.get('bidvalue'))
            if val < 0:
                val=0
            if val > team.account:
                val = team.account
            pk_to_drop  = request.POST.get('Drop')
            dropee      = Player.objects.get(pk=pk_to_drop)
            priority    = int(request.POST.get('Priority'))
            # priority can not be the same as any other unprocessed bids with same drop
            same_drop   = Bid.objects.filter(team=team).filter(processed=False).filter(drop=dropee)
            other_prios = []            
            for sd in same_drop:
                other_prios.append(sd.priority)
            while priority in other_prios:
                priority += 1
            b           = Bid(team=team, amount=val, player=p, drop=dropee, priority=priority)
            b.save()
            return HttpResponseRedirect("/team")
        else:
            return render(request, 'bid.html', {'player': p, 'roster':roster, 'team':team})
    else:
        return HttpResponseRedirect("/")

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
        
def week_results(request, week=None):
    u               = request.user
    this_week       = util.waiver_week(timezone.now())
    has_permission  = (u.is_staff or u.is_superuser)
    # if week is defined - always show results. They will be processed
    # if it is None and it is second waiver period and user is staff allow week to stay None
    show_unprocessed = (not week) and has_permission and util.is_2_waiver_period()

    if week:
        week = int(week)
    # otherwise set week to this week so unprocessed bids are hidden
    elif not show_unprocessed:
        week = this_week - 1
        
    # request is post if commit_week was pressed - or someone sent a post-request by other means...
    if request.method == 'POST':
        # iff unprocessed is allowed to be shown, then the POST is also allowed to do processing
        if show_unprocessed:
            # unprocessed bids will be processed
            rounds, droplist = util.round_results(commit=True)
        return HttpResponseRedirect("/")
    else:        
        # if week is None, unprocessed bids will be shown
        rounds, droplist = util.round_results(week=week)
        return render(request, 'results.html', {'rounds':rounds, 
                                                'droplist':droplist, 
                                                'weeks': range( 1, this_week ), 
                                                'week':week}) # if week is none commit button appears
            