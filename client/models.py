from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Lobby(models.Model):
    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

