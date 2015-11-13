from django.contrib import admin

# Register your models here.

from .models import Team, Bid, Player


class BidsAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'drop', 'priority', 'processed','succesful','swapped_on_nfl','date')
    list_filter = ['succesful', 'processed', 'swapped_on_nfl']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'dflteam', 'position')
    list_filter = ['dflteam']
    
admin.site.register(Team)
admin.site.register(Bid, BidsAdmin)
admin.site.register(Player, PlayerAdmin)

