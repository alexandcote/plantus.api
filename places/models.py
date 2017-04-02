import uuid

from django.db import models
from django.db.models import ImageField

from plantus.settings.settings_share import AUTH_USER_MODEL


class Place(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    picture = ImageField(upload_to='places', default='default/place.jpg')
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name='places',
                                   blank=True)
    identifier = models.UUIDField(max_length=100, blank=False, null=False,
                                  unique=True, default=uuid.uuid4,
                                  db_index=True)

    def __str__(self):
        return self.name
