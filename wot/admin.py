from django.contrib import admin
from django.core import urlresolvers
from .models import *

class PlayerInline(admin.TabularInline):
    model = Player
    fieldsets = (
        ('Players', {
            'classes': ('collapse',),
            'fields': (('account_name', 'account_id')),
        }),
    )
@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    """
    Clan model
    """
    list_display = ('tag', 'name', 'clan_id',)

    inlines = [
        PlayerInline,
    ]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Tank model
    """

    list_display = ('short_name', 'tier', 'tank_id')


class PlayerDataInline(admin.TabularInline):
    model = PlayerData
    fieldsets = (
        ('Data', {
            'classes': ('collapse',),
            'fields': (
                       'joined_clan_date','battles_on_random',
                       'last_battle_time',
                       'week_resources_earned','total_resources_earned'),
        }),
    )

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Player admin
    """
    list_display = ('account_name', 'account_id')

    inlines = [
        PlayerDataInline,
    ]

@admin.register(PlayerData)
class PlayerDataAdmin(admin.ModelAdmin):

    list_display = ('player', 'created',)
    list_filter = ('player', 'created',)
    search_fields = ('player',)

