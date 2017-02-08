from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Lobby
from .forms import CreateLobbyForm


def index(request):
    return render(request, 'client/index.html', {})


def lobbies(request):
    # get lobbies and render view for lobbies
    try:
        lobbies_list = Lobby.objects.get()
    except Lobby.DoesNotExist:
        lobbies_list = []

    return render(request, 'client/lobbies.html', {'lobbies': lobbies_list})


def createlobby(request):
    if request.method == "POST":
        form = CreateLobbyForm(request.user, request.POST)
        # form.created_by_id = request.user.id
        # print('posting', form.created_by_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/client/lobbies/")
    else:
        form = CreateLobbyForm()

    return render(request, 'client/lobby_create.html', {'form': form})

