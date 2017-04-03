from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.db.models import Count
from django.shortcuts import render, redirect
from .models import Lobby, LobbyUserMap
from django.contrib.auth.models import User
from .forms import CreateLobbyForm


@login_required(login_url='/accounts/login/')
def game(request):
    lobby_map = LobbyUserMap.objects.get(user=request.user)
    l_maps = LobbyUserMap.objects.filter(lobby=lobby_map.lobby)
    context = {
        'maps': l_maps,
    }
    return render(request, 'client/game.html', context)

@login_required(login_url='/accounts/login/')
def start(request):

    lobby_map = LobbyUserMap.objects.get(user=request.user)
    lobby = Lobby(lobby=lobby_map.lobby)

    if lobby.started:
        # redirect to game if already started
        return HttpResponseRedirect('client/game')
    elif lobby_map.is_admin:
        lobby.started = True
        lobby.commit()

    return HttpResponseRedirect('client/game')


@login_required(login_url='/accounts/login/')
def lobby_list(request):
    # get lobbies and render view for lobbies
    try:
        lobbies = Lobby.objects.annotate(player_count=Count('lobbyusermap__user'))
    except Lobby.DoesNotExist:
        lobbies = []

    return render(request, 'client/lobby_list.html', {'lobbies': lobbies})


@login_required(login_url='/accounts/login/')
def lobby_create(request):
    if request.method == "POST":
        form = CreateLobbyForm(request.POST)

        if request.user.is_authenticated() and form.is_valid():
            lobby = form.save()

            # create map for user
            map = LobbyUserMap(is_admin=True, user = request.user, lobby=lobby)
            map.commit()

            return HttpResponseRedirect("/client/lobby/join/{0}".format(lobby.id))
    else:
        form = CreateLobbyForm()

    return render(request, 'client/lobby_create.html', {'form': form})


@login_required(login_url='/accounts/login/')
def lobby_join(request, lobby_id):
    if request.user.is_authenticated():
        # remove all current lobby maps for user
        LobbyUserMap.objects.filter(user=request.user).delete()

        # add lobby map
        model = LobbyUserMap(user=request.user, lobby=Lobby.objects.get(id=lobby_id))
        model.save()
        return HttpResponseRedirect("/client/lobby/{0}".format(lobby_id))

    return HttpResponseRedirect("/accounts/login/")


@login_required(login_url='/accounts/login/')
def lobby_leave(request, lobby_id):
    if request.user.is_authenticated():

        LobbyUserMap.objects.filter(user=request.user, lobby=Lobby.objects.get(id=lobby_id)).delete() # delete lobby map

    return redirect('client:lobby_list')

@login_required(login_url='/accounts/login/')
def lobby(request, lobby_id):
    try:
        lobby_map = LobbyUserMap.objects.get(user=request.user, lobby=lobby_id)
        if request.user.is_authenticated():
            lobby_model = Lobby.objects.get(id=lobby_id)
            players = User.objects.filter(lobbyusermap__lobby=lobby_id)
            context = {
                'is_admin': lobby_map.is_admin,
                'lobby': lobby_model,
                'players': players
            }
            return render(request, "client/lobby.html", context)
        else:
            raise Http404("Authentication failed")

    except ObjectDoesNotExist:
        return HttpResponseRedirect("/client/lobby/list")


