from django.contrib.auth.models import User
from django.db import models


class Place(models.Model):
    name = models.TextField()
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    users = models.ManyToManyField(User, related_name='Place')

    def __str__(self):
        return self.name
