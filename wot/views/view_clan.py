from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from wot.models import Clan, PlayerData

def clan_detail(request, tag):

    clan = get_object_or_404(Clan,
                             tag=tag)

    members = clan.get_members()

    return render(request,
                  'wot/clan/clan_detail.html',
                  {'clan':clan,
                   'members':members,
                   }
                  )


def clan_list(request):
    clans = Clan.objects.all()

    clans_members = {clan: clan.get_members() for clan in clans}

    # for clan, members in clans_members.items():
    #     for member in members:
    #         data = PlayerData.objects.

    return render(request,
                  'wot/clan/clan_list.html',
                  {'clans_members': clans_members
                   })

def one_day_stats(player):
    now = timezone.now()
    yesteday = now.date() - timezone.timedelta(days=1)

    today_stats = PlayerData.objects.filter(created__day=now.date())
    yesterday_stats = 1



