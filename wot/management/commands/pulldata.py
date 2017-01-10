from django.core.management.base import BaseCommand, CommandError
from wot.models import *
import wargaming
import json


class Command(BaseCommand):
    _appID = '3bab986f0bd5a381dfacf4ca9b639fa4'
    wgwot = wargaming.WoT(_appID, region='eu', language='en')
    wgwgn = wargaming.WGN(_appID, region='eu', language='en')
    anv_clanid = 500004323
    pomlcky_clanid = 500054759
    anv_v_clanid = 500075469

    def handle(self, *args, **options):
        self.stdout.write("command!")

        # clans = self.download_and_clean()
        with open('data.json','r') as inf:
          clans = json.load(inf,parse_int=str, parse_float=str)

        for clan_id, clan_data in clans.items():

            # create clans
            clan, result = Clan.objects.update_or_create(clan_id=clan_id,
                                                         name=clan_data['name'],
                                                         tag=clan_data['tag'])

            # create / update player data
            for member_id, member_data in clan_data['members'].items():
                player, result = Player.objects.update_or_create(account_id=member_data['account_id'],
                                                                 account_name=member_data['account_name'],
                                                                 clan=clan)

                # print(type(member_data['stronghold']['week_resources_earned']),
                #       member_data['stronghold']['week_resources_earned'])
                # input()
                # print(type(member_data['joined_clan_date']), member_data['joined_clan_date'])

                jcd = timezone.datetime.fromtimestamp(float(member_data['joined_clan_date']))
                lbt = timezone.datetime.fromtimestamp(float(member_data['last_battle_time']))

                player_data, result = PlayerData.objects. \
                    update_or_create(player=player,
                                     joined_clan_date=jcd,
                                     last_battle_time=lbt,
                                     role_in_clan=member_data['role'],
                                     battles_on_random=member_data['statistics']['random']['battles'],
                                     battles_all=member_data['statistics']['all']['battles'],
                                     battles_stronghold=member_data['stronghold']['stronghold_skirmish']['battles'],

                                     total_resources_earned=member_data['stronghold']['total_resources_earned'],
                                     # week_resources_earned=wk,
                                     )

    def download_and_clean(self):
        data = {}
        # keys
        # clans['clan_id']
        # members, players ['account_id']
        # return dict
        # {'clan_id': {'tag': 'TAG',
        #              'name': 'CLANNAME',
        #              'members': {'account_id': {'stronghold': {'stronghold_skirmish': {'battles': 2219},
        #                                                        'total_resources_earned': 32502,
        #                                                        'week_resources_earned': 0},
        #                                         'last_battle_time': 1483682632,
        #                                         'statistics': {'all': {'battles': 70507},
        #                                                        'random': {'battles': 67313}
        #                                                        },
        #                                         'account_id': 'number',
        #                                         'account_name': 'NickNam3',
        #                                         'joined_at': 1447589992,
        #                                         'role': 'Private'
        #                                         },
        #                          'player2': {},
        #                          }
        #              }
        #  }

        # 1.st request
        clans = self.wgwgn.clans.info(clan_id=[self.anv_v_clanid,
                                               self.anv_clanid,
                                               self.pomlcky_clanid],
                                      fields=['tag', 'name', 'members'])

        for clan_id, clan_data in clans.items():
            data[clan_id] = {'members': {},
                             'tag': clan_data['tag'],
                             'name': clan_data['name']}
            member_ids = [member['account_id'] for member in clan_data['members']]
            # 2.nd request
            players_info = self.wgwot.account.info(account_id=member_ids,
                                                   fields=['last_battle_time',
                                                           'statistics.all.battles',
                                                           'statistics.random.battles',
                                                           ],
                                                   extra=['statistics.random']).data

            # 3.rd request
            player_stronghold = self.wgwot.stronghold.accountstats(account_id=member_ids,
                                                                   fields=['stronghold_skirmish.battles',
                                                                           'total_resources_earned',
                                                                           'week_resources_earned',
                                                                           ])

            # iterate through members and merge data from clan, stronghold and info
            for idx, member_id in enumerate(member_ids):
                account_id = str(member_id)

                if player_stronghold[account_id]['stronghold_skirmish'] is None:
                    # print(account_id)
                    # print(player_stronghold[account_id]['stronghold_skirmish'])
                    player_stronghold[account_id]['stronghold_skirmish'] = {"battles": 0}
                    # print(player_stronghold[account_id]['stronghold_skirmish'])

                player = {'stronghold': player_stronghold[account_id],
                          'last_battle_time': players_info[account_id]['last_battle_time'],
                          'statistics': players_info[account_id]['statistics'],
                          'account_id': account_id,
                          'role': clan_data['members'][idx]['role_i18n'],
                          'joined_clan_date': clan_data['members'][idx]['joined_at'],
                          'account_name': clan_data['members'][idx]['account_name']
                          }

                data[clan_id]['members'][account_id] = player

        self.stdout.write('writing json')
        with open('data.json', 'w+') as outf:
            json.dump(data, outf, indent=2, sort_keys=True, separators=(',', ': '))

        with open('data.json', 'r') as inf:
            return json.load(inf, parse_float=str, parse_int=str)
