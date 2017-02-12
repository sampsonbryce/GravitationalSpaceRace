from django.db import models
from django.conf import settings


# Create your models here.
class Lobby(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)


class LobbyUserMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    lobby = models.ForeignKey(Lobby)

