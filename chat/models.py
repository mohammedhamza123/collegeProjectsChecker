from django.db import models

from api.models import Project
from django.conf.global_settings import AUTH_USER_MODEL

# Create your models here.


class Channel(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    members = models.ManyToManyField(AUTH_USER_MODEL)


class Messege(models.Model):
    context = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    time_sent = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.Channel}:{self.sender}"
