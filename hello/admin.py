from django.contrib import admin

# Register your models here.

from .models import Team, Bid, Player



class BidsAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'drop', 'priority', 'processed','succesful','swapped_on_nfl','date')
    list_filter  = ['succesful', 'processed', 'swapped_on_nfl']
    actions      = ['make_swapped', 'make_processed']

    def make_swapped(admin, req, queryset):
        queryset.update(swapped_on_nfl=True)
    make_swapped.short_description = 'Set as swapped on NFL'
    def make_processed(admin, req, queryset):
        queryset.update(processed=True)
    make_processed.short_description = 'Set as processed'


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'dflteam', 'position')
    list_filter = ['dflteam']
    
admin.site.register(Team)
admin.site.register(Bid, BidsAdmin)
admin.site.register(Player, PlayerAdmin)

