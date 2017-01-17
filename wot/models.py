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
    # why are you creating your own primary key?
    clan_id = models.IntegerField(primary_key=True)
    # are you sure these can be empty?
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=5)

    # query manager
    # this is set by default, there is no need for this
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
    # I think a CharField would be better here. You can also add some validation there
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
    # isn't this an epoch? So it can be an IntegerField
    access_token_expires_at = models.CharField(max_length=10,
                                               blank=True,
                                               null=True)
    account_name = models.CharField(max_length=250)

    # think about formatting. Flake8 is your friend
    # members is a bit weird as a related_name. Since it's clans which are referred to, right?
    # and members are a specific key in clan
    clan = models.ForeignKey('Clan',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                             related_name='members')

    # shouldn't this be an ForeignKey as well?
    previous_clan_id = models.IntegerField(verbose_name='Previous Clan',
                                           blank=True,
                                           null=True)



    def __str__(self):
        return '{0} - {1}'.format(self.account_name, self.account_id)

    def get_absolute_url(self):
        return reverse('wot:player_detail',
                       args=[self.account_name])

    class Meta:
        ordering = ['account_name']

class PlayerData(models.Model):
    """
    Players data daily tracked
    """
    # if you find yourself adding this field to a lot of models.
    # You can consider creating a base model with this field
    # btw why is created here? isn't this supposed to be part of the Player model?
    created = models.DateTimeField(auto_now_add=True)

    # a related name with the same name as the key is not necessary
    player = models.ForeignKey('Player',
                               on_delete=models.CASCADE,
                               related_name='player',
                               null=True,
                               blank=True
                               )
    # if it's just a date you want to store. You can also use a DateField
    joined_clan_date = models.DateTimeField(blank=True,
                                             null=True)
    # consider adding a ChoiceField and add a list of Choices on top of the model
    role_in_clan = models.CharField(max_length=250,
                                    blank=True,
                                    null=True)
    # isn't this supposed to be a BooleanField?
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

    class Meta:
        get_latest_by ='created'
        ordering = ['-created']
