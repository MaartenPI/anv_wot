import json

from django.test import TestCase
from .models import *


class ClanTest(TestCase):
    def setup(self):
        clan_data = {'500004323': {'members': [{'account_id': 501435906,
                                                'account_name': 'NoSmallCZ',
                                                'joined_at': 1447589992,
                                                'role': 'private',
                                                'role_i18n': 'Private'},
                                               {'account_id': 519375275,
                                                'account_name': 'aiznem1',
                                                'joined_at': 1459356339,
                                                'role': 'private',
                                                'role_i18n': 'Private'}],
                                   'name': 'Acta non Verba',
                                   'tag': 'ANV'}}
        # create clans
        for clan_id, data in clan_data.items():
            clan = {'tag': data['tag'],
                    'name': data['name'],
                    'clan_id': clan_id}

            Clan.objects.update_or_create(**clan)

        def test_clan_exist(self):
            clan = Clan.objects.get(clan_id='500004323')

            self.assertEquals(clan.clan_id, '500004323')
            self.assertEquals(clan.name, 'Acta non Verba')
            self.assertEquals(clan.tag, 'ANV')


class PlayerTest(TestCase):
    """
    Tests creating of player from clan member list
    """

    def setUp(self):

        clan_data = {'500004323': {'members': [{'account_id': 501435906,
                                                'account_name': 'NoSmallCZ',
                                                'joined_at': 1447589992,
                                                'role': 'private',
                                                'role_i18n': 'Private'},
                                               {'account_id': 519375275,
                                                'account_name': 'aiznem1',
                                                'joined_at': 1459356339,
                                                'role': 'private',
                                                'role_i18n': 'Private'}],
                                   'name': 'Acta non Verba',
                                   'tag': 'ANV'}}
        # create clans
        for clan_id, data in clan_data.items():
            clan = {'tag': data['tag'],
                    'name': data['name'],
                    'clan_id': clan_id}

            Clan.objects.update_or_create(**clan)
            # create players
            for member in data['members']:
                player_info = {'account_id': member['account_id'],
                               'nickname': member['account_name']}
                player, res = Player.objects.update_or_create(**player_info)

                tz_fromtimestamp = timezone.datetime.fromtimestamp

                PlayerData.objects.update_or_create(playe=player,
                                                    joined_clan_date=tz_fromtimestamp(member['account_name']),
                                                    role_in_clan=member['role_i18n'])

    def test_player_exist(self):
        player = Player.objects.get(account_id=501435906)
        self.assertEquals(player.account_id, 501435906)
        self.assertEquals(player.nickname, 'NoSmallCZ')


class PlayerDataTest(TestCase):

    def setup(self):
        player = Player.objects.create(account_id=501435906,
                                        nickname='NoSmallCZ')

        member = {  'account_id': 501435906,
                    'account_name': 'NoSmallCZ',
                    'joined_at': 1447589992,
                    'role': 'private',
                    'role_i18n': 'Private'}

        tz_fromtimestamp = timezone.datetime.fromtimestamp
        PlayerData.objects.update_or_create(playe=player,
                                            joined_clan_date=tz_fromtimestamp(member['account_name']),
                                            role_in_clan=member['role_i18n'])

    def test_player_data(self):
        player = Player.objects.get(account_id=501435906)


class VehicleTest(TestCase):
    pass
