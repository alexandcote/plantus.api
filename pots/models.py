import uuid

from django.db import models

from places.models import Place
from plants.models import Plant

from django.utils.translation import ugettext_lazy as _


class Pot(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    identifier = models.UUIDField(max_length=100, blank=False, null=False,
                                  unique=True, default=uuid.uuid4,
                                  db_index=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              blank=None, null=None, related_name='pots')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE,
                              blank=None, null=None, related_name='pots')

    def __str__(self):
        """
         Display the pot object
        """
        return self.name


class TimeSerie(models.Model):

    pot = models.ForeignKey(Pot, on_delete=models.CASCADE, blank=None,
                            null=None, related_name='timeseries')
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    temperature = models.DecimalField(
        blank=False, null=False, verbose_name=_('Temperature'),
        max_digits=4, decimal_places=2
    )
    humidity = models.DecimalField(
        blank=False, null=False, verbose_name=_('Humidity'),
        max_digits=4, decimal_places=2
    )
    luminosity = models.DecimalField(
        blank=False, null=False, verbose_name=_('Luminosity'),
        max_digits=4, decimal_places=2
    )
    water_level = models.DecimalField(
        blank=False, null=False, verbose_name=_('Water level'),
        max_digits=4, decimal_places=2
    )

    def __str__(self):
        """
         Display the time serie object
        """
        return "{0} - {1}".format(self.pot, self.date)
