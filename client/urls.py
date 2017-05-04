from django.conf.urls import url

from . import views

app_name = 'client'
urlpatterns = [
    url(r'^$', views.game, name='game'),
    url(r'^lobby/start/?$', views.lobby_start, name='lobby_start'),
    url(r'^lobby/list/?$', views.lobby_list, name='lobby_list'),
    url(r'^lobby/list/data$', views.lobby_list_data, name='lobby_list_data'),
    url(r'^lobby/create/$', views.lobby_create, name='lobby_create'),
    url(r'^lobby/join/([0-9]+)/$', views.lobby_join, name='lobby_join'),
    url(r'^lobby/leave/([0-9]+)/$', views.lobby_leave, name='lobby_leave'),
    url(r'^lobby/([0-9]+)/$', views.lobby, name='lobby'),
    url(r'^lobby/([0-9]+)/data/?$', views.lobby_data, name='lobby_data'),
]
