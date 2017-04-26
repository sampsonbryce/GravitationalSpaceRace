from django.db import models
from django.conf import settings


# Create your models here.
class Lobby(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    started = models.BooleanField(default=False)

    def _get_player_count(self):
        return len(LobbyUserMap.objects.filter(lobby=self))
    player_count = property(_get_player_count)



class LobbyUserMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    lobby = models.ForeignKey(Lobby)
    is_admin = models.BooleanField(default=False)

