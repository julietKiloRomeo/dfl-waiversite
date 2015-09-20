from django.shortcuts import render
#from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Greeting
import util
from django.contrib import auth

#import os

# Create your views here.
def index(request):
    trades = util.latest_trades()
    return render(request, 'index.html', {'trades': trades})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def bid(request):
    return render(request, 'index.html', {'trades': ['bid']})

def rules(request):
    return render(request, 'index.html', {'trades': ['150$']})



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