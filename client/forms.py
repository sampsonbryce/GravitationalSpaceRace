from django.forms import ModelForm
from .models import Lobby


class CreateLobbyForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        self.created_by = user
        super(CreateLobbyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lobby
        fields = ['name']

