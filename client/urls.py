from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lobbies/$', views.lobbies, name='lobbies'),
    url(r'^lobbies/create/$', views.createlobby, name='createlobby'),

]
