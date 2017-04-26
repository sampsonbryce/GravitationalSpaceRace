from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lobby, LobbyUserMap
from django.contrib.auth.models import User
from .forms import CreateLobbyForm
from django.contrib import messages
from django.core import serializers
from core.helpers import JsonSerialize
import re, json

def lobby_navbar(request):
    context = {}

    map = LobbyUserMap.objects.filter(user=request.user)
    if map.count() > 0:
        lobby = map.get().lobby
        context["display_lobby_navbar"] = True
        context["lobby"] = lobby

    print("full path:", request.get_full_path())
    if re.match(r'^/client/lobby/[0-9]+/$', request.get_full_path()) is not None:
        context["display_lobby_navbar"] = False

    return context


@login_required(login_url='/accounts/login/')
def game(request):
    lobby_map = LobbyUserMap.objects.get(user=request.user)
    l_maps = LobbyUserMap.objects.filter(lobby=lobby_map.lobby)
    context = {
        'maps': l_maps,
    }
    return render(request, 'client/game.html', context)

@login_required(login_url='/accounts/login/')
def lobby_start(request):
    lobby_map = LobbyUserMap.objects.get(user=request.user)
    lobby = Lobby.objects.get(id=lobby_map.lobby.id)

    if lobby.started:
        # redirect to game if already started
        return redirect('client:game')
    elif lobby_map.is_admin:
        lobby.started = True
        lobby.save()

    return redirect('client:game')


@login_required(login_url='/accounts/login/')
def lobby_list(request):
    return render(request, 'client/lobby_list.html')

@login_required(login_url='/accounts/login/')
def lobby_list_data(request):
    # get lobbies and render view for lobbies
    lobbies = []
    try:
        lobbies_list = Lobby.objects.all()
        for lobby in lobbies_list:
            if lobby.player_count == 0:
                LobbyUserMap.objects.filter(lobby=lobby).delete()
                lobby.delete()
            else:
                lobby_dict = model_to_dict(lobby)
                lobby_dict['player_count'] = lobby.player_count
                lobby_dict['created_date'] = lobby.created_date.__str__()
                lobby_dict['created_by'] = lobby.created_by.username
                lobbies.append(lobby_dict)
    except Lobby.DoesNotExist:
        pass

    map = LobbyUserMap.objects.filter(user=request.user)
    if map.count() > 0:
        my_lobby = map.get().lobby.id
    else:
        my_lobby = -1

    context = {
        'lobbies': lobbies,
        'my_lobby': my_lobby
    }
    return JsonResponse(context)

@login_required(login_url='/accounts/login/')
def lobby_create(request):
    if request.method == "POST":
        form = CreateLobbyForm(request.POST)

        if request.user.is_authenticated() and form.is_valid():
            lobby = form.save(commit=False)
            lobby.created_by = request.user
            lobby.save()


            # if user is in lobby already
            LobbyUserMap.objects.filter(user=request.user).delete() # delete lobby map

            # create map for user
            map = LobbyUserMap(is_admin=True, user=request.user, lobby=lobby)
            map.save()

            return HttpResponseRedirect("/client/lobby/join/{0}".format(lobby.id))
    else:
        form = CreateLobbyForm()

    return render(request, 'client/lobby_create.html', {'form': form})

@login_required(login_url='/accounts/login/')
def lobby_join(request, lobby_id):
    if request.user.is_authenticated():
        lobby = get_object_or_404(Lobby, id=lobby_id)

        map = LobbyUserMap.objects.filter(user=request.user)
        if lobby.started:
            if map.count() == 0:
                print("No maps, redirecting")
                messages.error(request, "Cannot join a lobby where the game has started, unless you were already in lobby")
                return HttpResponseRedirect("/client/lobby/list")
            else:
                if map.get().lobby.id != lobby_id:
                    print("Not in lobby, redirecting")
                    messages.error(request, "Cannot join a lobby where the game has started, unless you were already in lobby")
                    return HttpResponseRedirect("/client/lobby/list")
                else:
                    return HttpResponseRedirect("/client")
        else:
            # remove all current lobby maps for user
            if map.get().lobby.id != lobby_id:
                map.delete()

        # make admin if only person in lobby
        is_admin = False
        try:
            maps = LobbyUserMap.objects.filter(lobby=lobby_id)
            maps.get()
        except LobbyUserMap.DoesNotExist:
            is_admin = True

        # add lobby map
        model = LobbyUserMap(user=request.user, lobby=Lobby.objects.get(id=lobby_id), is_admin=is_admin)
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
            return render(request, "client/lobby.html", {})
        else:
            raise Http404("Authentication failed")

    except ObjectDoesNotExist:
        return HttpResponseRedirect("/client/lobby/list")

def lobby_data(request, lobby_id):
    try:
        lobby_map = LobbyUserMap.objects.get(user=request.user, lobby=lobby_id)
        if request.user.is_authenticated():
            lobby_model = Lobby.objects.get(id=lobby_id)
            lobby_dict = JsonSerialize(lobby_model)
            lobby_dict["created_by"] = lobby_model.created_by.username
            players = User.objects.filter(lobbyusermap__lobby=lobby_id)
            player_list = JsonSerialize(players)
            for player in player_list:
                print(player)

            context = {
                'is_admin': lobby_map.is_admin,
                'lobby': lobby_dict,
                'players': player_list
            }
            return JsonResponse(context)
        else:
            return JsonResponse({"message":"Authentication failed"})
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Failed to load lobby"})

