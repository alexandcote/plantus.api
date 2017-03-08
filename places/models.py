from django.db import models

from plantus.settings.settings_share import AUTH_USER_MODEL


class Place(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    users = models.ManyToManyField(AUTH_USER_MODEL, related_name='places',
                                   blank=True)

    def __str__(self):
        return self.name
