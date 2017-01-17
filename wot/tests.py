# Bonus points for adding a test
from django.core.management import call_command
from django.test import TestCase
from .models import *
import os
from wot.management.commands import pulldata
import json

class PulldataCommandTest(TestCase):

    def setUp(self):
        self.folder = 'wot/testdata'
        self.clan_file = os.path.relpath('wot/testdata/wg_clans_response.json', start=os.curdir)
        self.test_datafile = 'wot/testdata/old_data.json'
        self.created_datafile = 'wot/testdata/created_data.json'

    # awww, why did you not give it a proper name?
    def test_asd(self):
        testfilename = 'wot/testdata/created_data.json'
        call_command(pulldata.Command(), json=testfilename)

        with open('wot/testdata/old_data.json', 'r') as oldf:
            old_file = json.load(oldf, parse_int=str, parse_float=str)

        with open(testfilename, 'r') as nef:
            created_file = json.load(nef, parse_int=str, parse_float=str)

# class ClanTest(TestCase):
#     def setup(self):
#         clan_data = {'500004323': {'members': [{'account_id': 501435906,
#                                                 'account_name': 'NoSmallCZ',
#                                                 'joined_at': 1447589992,
#                                                 'role': 'private',
#                                                 'role_i18n': 'Private'},
#                                                {'account_id': 519375275,
#                                                 'account_name': 'aiznem1',
#                                                 'joined_at': 1459356339,
#                                                 'role': 'private',
#                                                 'role_i18n': 'Private'}],
#                                    'name': 'Acta non Verba',
#                                    'tag': 'ANV'}}
#         # create clans
#         for clan_id, data in clan_data.items():
#             clan = {'tag': data['tag'],
#                     'name': data['name'],
#                     'clan_id': clan_id}
#
#             Clan.objects.update_or_create(**clan)
#
#         def test_clan_exist(self):
#             clan = Clan.objects.get(clan_id='500004323')
#
#             self.assertEquals(clan.clan_id, '500004323')
#             self.assertEquals(clan.name, 'Acta non Verba')
#             self.assertEquals(clan.tag, 'ANV')
#
#
# class PlayerTest(TestCase):
#     """
#     Tests creating of player from clan member list
#     """
#
#     # TODO cover player is in clan
#     # TODO cover player is entered clan
#     # TODO cover player left clan
#
#     def setUp(self):
#
#         self.clan_data = {'500004323': {'members': [{'account_id': 501435906,
#                                                 'account_name': 'NoSmallCZ',
#                                                 'joined_at': 1447589992,
#                                                 'role': 'private',
#                                                 'role_i18n': 'Private'},
#                                                {'account_id': 519375275,
#                                                 'account_name': 'aiznem1',
#                                                 'joined_at': 1459356339,
#                                                 'role': 'private',
#                                                 'role_i18n': 'Private'}],
#                                    'name': 'Acta non Verba',
#                                    'tag': 'ANV'}}
#         # create clans
#         for clan_id, data in clan_data.items():
#             clan = {'tag': data['tag'],
#                     'name': data['name'],
#                     'clan_id': clan_id}
#
#             Clan.objects.update_or_create(**clan)
#             # create players
#             for member in data['members']:
#                 player_info = {'account_id': member['account_id'],
#                                'nickname': member['account_name']}
#                 player, res = Player.objects.update_or_create(**player_info)
#
#                 tz_fromtimestamp = timezone.datetime.fromtimestamp
#
#                 PlayerData.objects.update_or_create(playe=player,
#                                                     joined_clan_date=tz_fromtimestamp(member['account_name']),
#                                                     role_in_clan=member['role_i18n'])
#
#     def test_player_exist(self):
#         player = Player.objects.get(account_id=501435906)
#         self.assertEquals(player.account_id, 501435906)
#         self.assertEquals(player.nickname, 'NoSmallCZ')
#
#
# class PlayerDataTest(TestCase):
#
#     def setup(self):
#         player = Player.objects.create(account_id=501435906,
#                                         nickname='NoSmallCZ')
#
#         member = {  'account_id': 501435906,
#                     'account_name': 'NoSmallCZ',
#                     'joined_at': 1447589992,
#                     'role': 'private',
#                     'role_i18n': 'Private'}
#
#         tz_fromtimestamp = timezone.datetime.fromtimestamp
#         PlayerData.objects.update_or_create(playe=player,
#                                             joined_clan_date=tz_fromtimestamp(member['account_name']),
#                                             role_in_clan=member['role_i18n'])
#
#     def test_player_data(self):
#         player = Player.objects.get(account_id=501435906)
#
#
