from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from wot.models import PlayerData, Clan, Player
import wargaming
import json
import os

class Command(BaseCommand):
    # Store credentials in your settings-file
    # Also be aware of abuse of keys in public github repos
    _appID = '3bab986f0bd5a381dfacf4ca9b639fa4'
    wgwot = wargaming.WoT(_appID, region='eu', language='en')
    wgwgn = wargaming.WGN(_appID, region='eu', language='en')
    anv_clanid = 500004323
    pomlcky_clanid = 500054759
    anv_v_clanid = 500075469

    def add_arguments(self, parser):

        # use local files
        parser.add_argument(
            '--folder',
            default='wot/testdata',
            nargs='?',
            help='Use files from local directory instead downloading data from WG API',
        )
        # json output
        parser.add_argument(
            '--json',
            default='wot_clean_data.json',
            # nargs=1,
            help='Save output to json',
        )

    def handle(self, *args, **options):
        """
        Main command function
        :param args: arguments
        :param options:  optional arguments
        """

        # clean all data and store it in dictionary
        clans = self.merge_and_clean(*args, **options)

        # dump the the result to json and quit
        if options['json']:
            filename = os.path.relpath(options['json'])

            with open(filename, 'w+') as outf:
                json.dump(clans, outf, indent=2, sort_keys=True, separators=(',', ': '))
            rtn = "Saved to file {fn}".format(fn=filename)
            self.stdout.write(rtn)
            return

        # update the database with the records
        self.update_database(clans)

    # I see a lot of happy path here. You are assuming your code works and never breaks.
    # But what if it does?
    def update_database(self, clans):
        """
        Updates database entries
        :param clans: output from merge_and_clean
        """

        for clan_id, clan_data in clans.items():

            # create clans
            clan, created = Clan.objects.update_or_create(clan_id=clan_id,
                                                          name=clan_data['name'],
                                                          tag=clan_data['tag'])
            if created:
                log = 'Created clan {tag}, {cid}'.format(tag=clan.tag, cid=clan.clan_id)
                self.stdout(log)

            downloaded_member_ids = set(member['account_id'] for member in clan_data['members'])
            stored_member_ids = set(clan.get_members().values_list('account_id', flat=True))

            newcomers = downloaded_member_ids - stored_member_ids
            left_clan = stored_member_ids - downloaded_member_ids

            self.remove_leavers(left_clan)

            # create / update player data
            for member_id, member_data in clan_data['members'].items():
                player, created = Player.objects.update_or_create(account_id=member_data['account_id'],
                                                                  account_name=member_data['account_name'],
                                                                  clan=clan)
                if created:
                    log = 'Created player {nick}, {aid}'.format(nick=player.account_name,
                                                                aid=player.account_id)
                    # Usually you would use a logger instead of relying on stdout
                    self.stdout(log)

                # Naming your variables is important. This is hard to read
                jcd = timezone.datetime.fromtimestamp(float(member_data['joined_clan_date']))
                lbt = timezone.datetime.fromtimestamp(float(member_data['last_battle_time']))

                player_data, created = PlayerData.objects. \
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
                if created:
                    log = 'Created player data {nick}, {date}'.format(nick=player.account_name,
                                                                      date=player_data.created)
                    self.stdout(log)


    def merge_and_clean(self, *args, **options):
        # try not to place vars in the middle of nowhere. it makes it hard to read
        # what's going on
        data = {}
        
        # Remove commented code
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

        # Consider placing the codeblocks in a separate functions instead of long blocks of code
        if options['folder']:

            folder = os.path.relpath(options['folder'])

            with open(os.path.join(folder,'wg_clans_response.json'), 'r') as icf:
                clans = json.load(icf, parse_constant=str, parse_int=str, parse_float=str)


        else:
            # response containing new members
            clans = self.clean_clans([self.anv_v_clanid, self.anv_clanid, self.pomlcky_clanid],
                                     fields=['tag', 'name', 'members'])

        for clan_id, clan_data in clans.items():
            data[clan_id] = {'members': {},
                             'tag': clan_data['tag'],
                             'name': clan_data['name']}

            downloaded_member_ids = [member['account_id'] for member in clan_data['members']]

            # 2.nd request n times clan

            if options['folder']:
                pl_filename = 'wg_{tag}_players_response.json'.format(tag=clan_data['tag'])
                with open(os.path.join(folder, pl_filename), 'r') as pif:
                    players_info = json.load(pif, parse_constant=str, parse_int=str, parse_float=str)

                str_filename = 'wg_{tag}_stronghold_response.json'.format(tag=clan_data['tag'])

                with open(os.path.join(folder, str_filename), 'r') as sif:
                    player_stronghold = json.load(sif, parse_constant=str, parse_int=str, parse_float=str)


            else:
                players_info = self.clean_players(account_id=downloaded_member_ids,
                                                  # consider adding this list in a variable for readability
                                                  fields=['last_battle_time',
                                                          'statistics.all.battles',
                                                          'statistics.random.battles',
                                                          ],
                                                  extra=['statistics.random'])

                # 3.rd request n times clan
                player_stronghold = self.clean_player_stronghold(account_id=downloaded_member_ids,
                                                                 fields=['stronghold_skirmish.battles',
                                                                         'total_resources_earned',
                                                                         'week_resources_earned',
                                                                         ])

            # iterate through members and merge data from clan, stronghold and info
            for idx, member_id in enumerate(downloaded_member_ids):
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

        return data

    def clean_clans(self, clan_id_list, fields):
        """
        Download clans, tags, names, members+details
        :param clan_id_list: list of clan_ids
        :return: dictionary containing the data
        """
        # maybe explain what t and d mean
        default_clan = {'tag': 't',
                        'name': 'd',
                        'clan_id': 0}

        clans = self.wgwgn.clans.info(clan_id=clan_id_list,
                                      fields=fields)

        return clans if isinstance(clans, dict) else dict(clans)

    def clean_players(self, account_id, fields, extra):
        """
        Return players data in dict
        :param account_id: list of account_id
        :return: dictionary containing the data
        """
        players_info = self.wgwot.account.info(account_id=account_id,
                                               fields=fields,
                                               extra=extra).data

        return players_info if isinstance(players_info, dict) else dict(players_info)

    def clean_player_stronghold(self, account_id, fields):
        """
        Return player stronghold data
        :param account_id: :param account_id: list of account_id
        :param fields: fields from wg api
        :return: dictionary containing the data
        """
        player_stronghold = self.wgwot.stronghold.accountstats(account_id=account_id,
                                                               fields=fields)

        return player_stronghold if isinstance(player_stronghold, dict) else dict(player_stronghold)


    def remove_leavers(self, leavers):
        players = Player.objects.filter(account_id__in=leavers)
        # huh?
        pass
