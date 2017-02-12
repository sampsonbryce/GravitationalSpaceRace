from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Lobby


class CreateLobbyForm(ModelForm):
    # def __init__(self, user=None, *args, **kwargs):
        # if user is not None:
        #     print('setting created by', user.id)
        #     self.created_by = User.objects.get(id=user.id)
        #     print('created by', self.created_by)
        # super(CreateLobbyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lobby
        fields = ['name']

