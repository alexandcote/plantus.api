from django.db import models

from places.models import Place
from plants.models import Plant


class Pot(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              blank=None, null=None)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE,
                              blank=None, null=None)

    def __str__(self):
        """
         Display the pot object
        """
        return self.name
