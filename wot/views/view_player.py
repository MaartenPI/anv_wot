from wot.models import Player, PlayerData
from django.shortcuts import render, get_object_or_404

# import wargaming
# # Create your views here.
#
#
# def login_view(request):
#
#     appID = '3bab986f0bd5a381dfacf4ca9b639fa4'
#     actk = 'e2e75ff83fb1813b0cc1d8b171ae67e908fca25d'  # do 13.1 9:42
#     accID = '503577584'
#     wot = wargaming.WoT(appID, region='eu', language='en')
#     data = {'appID':appID,
#             'accID':accID}
#
#
#     return render(request, 'base.html', data)
#
# def resp_view(request):
#
#
#     data={}
#     if request.method == 'POST':
#         print('POST')
#         for key, value in request.POST.items():
#             print(key, value)
#
#     if request.method == 'GET':
#         print('GET')
#         for key, value in request.GET.items():
#             print(key,",", value)
#             data[key]=value
#
#     return render(request, 'wot/resp.html', {'data':data})

def model_field_values(model):
    for _field in model._meta.fields:
        if _field.name != 'id':
            yield _field.name, getattr(model, _field.name)



def player_list(request):
    players = Player.objects.all()

    return render(request, 'wot/player/player_list.html',{'players':players})

def player_detail(request, account_name):
    player = get_object_or_404(Player,
                               account_name=account_name)

    player_fields = list(model_field_values(player))

    player_data = PlayerData.objects.filter(player=player)

    player_data = [(data.created, model_field_values(data)) for data in player_data]

    # for x,y in player_data:
    #     print(x)
    #     for f in y:
    #         print(f)

    return render(request,
                  'wot/player/player_detail.html',
                  {'player':player,
                   'player_fields':player_fields,
                   'player_data':player_data
                   }
                  )

