from django.contrib import admin

# Register your models here.

from .models import Team, Bid, Player

admin.site.register(Team)
admin.site.register(Bid)
admin.site.register(Player)

