from django.shortcuts import render, get_object_or_404
from wot.models import Clan

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
    return render(request, 'wot/clan/clan_list.html', {'clans':clans})
