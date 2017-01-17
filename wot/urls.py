from django.conf.urls import url
import wot.views as views


urlpatterns = [
    # testing views

    # homepage
    url(r'^$', views.homepage, name='home'),

    # player views
    url(r'^players/$', views.player_list, name='players'),
    url(r'^player/(?P<account_name>[-\w]+)/$', views.player_detail, name='player_detail'),


    # clan views
    url(r'^clans/$', views.clan_list, name='clans'),
    url(r'^clan/(?P<tag>[-\w]+)/$', views.clan_detail, name='clan_detail'),


]