from django.shortcuts import render
#from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Greeting
import util
from django.contrib import auth
from models import Player, Team, Bid

#import os

# Create your views here.
def index(request):
    trades = util.latest_trades()
    N_bids = len(Bid.objects.filter(processed=False))
    return render(request, 'index.html', {'trades': trades, 'N':N_bids})

def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def bid(request, nfl_id):
    u       = request.user
    if u.is_authenticated():
        p       = Player.objects.get(nfl_id=nfl_id)
        if request.method == 'POST':
            team    = Team.objects.get(owner=u)
            val     = int(request.POST.get('bidvalue'))
            b = Bid(team=team, amount=val, player=p)
            b.save()
            return HttpResponseRedirect("/team")
        else:
            return render(request, 'bid.html', {'player': p})
    else:
        return HttpResponseRedirect("/login")

def team(request):
    u       = request.user
    if u.is_authenticated():
        team    = Team.objects.get(owner=u)
        bids    = Bid.objects.filter(team=team)
        return render(request, 'team.html', {'user': request.user, 'team':team, 'bids':bids})
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
    else:
        # Show an error page
        return HttpResponseRedirect("/invalid/")
        
        
        
def week_results(request):
    current_bids        = Bid.objects.filter(processed=False)

    bids    = {}    
    winners = {}    
    for b in current_bids:
        player = b.player.nfl_id
        bids.setdefault(player , []).append([b.amount, b, False])
    
    for p in bids.keys():
        sorted_bids = sorted(bids[p], key=lambda x:x[0], reverse=True)
        bids[p] = sorted_bids
        winner = util.bid_winner(bids[p])
        winners[p]=winner

    return render(request, 'results.html', {'bids':bids,'winners':winners})

    