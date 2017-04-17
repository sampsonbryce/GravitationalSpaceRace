from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Lobby


class CreateLobbyForm(ModelForm):
    class Meta:
        model = Lobby
        fields = ['name']

    # def save(self, commit=True):
    #     lobby = Lobby.save(commit)
    #     if commit:
    #         lobby.save()
    #
    #     return lobby


