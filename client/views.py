from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Lobby, LobbyUserMap
from .forms import CreateLobbyForm


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'client/index.html', {})


@login_required(login_url='/accounts/login/')
def lobby_list(request):
    # get lobbies and render view for lobbies
    try:
        lobbies = Lobby.objects.all()
    except Lobby.DoesNotExist:
        lobbies = []

    return render(request, 'client/lobby_list.html', {'lobbies': lobbies})


@login_required(login_url='/accounts/login/')
def lobby_create(request):
    if request.method == "POST":
        form = CreateLobbyForm(request.POST)

        if request.user.is_authenticated() and form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return HttpResponseRedirect("/client/lobby/list")
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
def lobby(request, lobby_id):
    try:
        lobby_map = LobbyUserMap.objects.get(user=request.user, lobby=lobby_id)
        if request.user.is_authenticated():
            lobby = Lobby.objects.get(id=lobby_id)
            context = {'lobby': lobby}
            return render(request, "client/lobby.html", context)

    except ObjectDoesNotExist:
        return HttpResponseRedirect("/client/lobby/list")


