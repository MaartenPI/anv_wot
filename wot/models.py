from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone


# class ClanMembersManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter(member='Player')


class Clan(models.Model):
    """
    Clan model
    """
    clan_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=5)

    # query manager
    objects = models.Manager()  # default manager

    def __str__(self):
        return "{tag}".format(tag=self.tag)

    def get_members(self):
        return Player.objects.filter(clan=self)

    def get_absolute_url(self):
        return reverse('wot:clan_detail',
                       args=[self.tag])

class Vehicle(models.Model):
    """
    Tank model
    """
    name = models.TextField()
    short_name = models.TextField()
    tank_id = models.IntegerField(primary_key=True)
    tier = models.IntegerField()

    def __str__(self):
        return self.name



class Player(models.Model):
    """
    Player model
    """
    account_id = models.IntegerField(primary_key=True)
    access_token = models.TextField(blank=True,
                                    null=True)
    access_token_expires_at = models.CharField(max_length=10,
                                               blank=True,
                                               null=True)
    account_name = models.CharField(max_length=250)

    clan = models.ForeignKey('Clan',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                             related_name='members')


    def __str__(self):
        return '{0} - {1}'.format(self.account_name, self.account_id)

    def get_absolute_url(self):
        return reverse('wot:player_detail',
                       args=[self.account_name])

class PlayerData(models.Model):
    """
    Players data daily tracked
    """
    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True,
    #                                editable=False,
    #                                blank=True
    #                                )
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE,
                               related_name='data',
                               null=True,
                               blank=True
                               )


    joined_clan_date = models.DateTimeField(blank=True,
                                             null=True)

    role_in_clan = models.CharField(max_length=250,
                                    blank=True,
                                    null=True)

    battles_on_random = models.IntegerField(blank=True,
                                               null=True)
    battles_all = models.IntegerField(blank=True,
                                      null=True)
    battles_stronghold = models.IntegerField(blank=True,
                                             null=True)

    tank = models.ManyToManyField('Vehicle',
                                    related_name='tanks',
                                    blank=True,)

    last_battle_time = models.DateTimeField(blank=True,
                                             null=True)
    # stronghold stats
    total_resources_earned = models.IntegerField(blank=True,
                                                 null=True)

    week_resources_earned = models.IntegerField(blank=True,
                                                 null=True)

    def __str__(self):
        return '{player}, {cr}'.format(player=self.player.account_name,
                                       cr=self.created)