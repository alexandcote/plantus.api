from django.db import models
from django.utils.translation import ugettext_lazy as _


class Plant(models.Model):
    name = models.CharField(
        max_length=255, blank=False, null=False, verbose_name=_('Name'))
    description = models.TextField(
        blank=False, null=False, verbose_name=_('Description'))
    humidity_spec = models.DecimalField(
        blank=False, null=False, verbose_name=_('Humidity spec'),
        max_digits=4, decimal_places=2)
    luminosity_spec = models.DecimalField(
        blank=False, null=False, verbose_name=_('Luminosity spec'),
        max_digits=4, decimal_places=2)
    temperature_spec = models.DecimalField(
        blank=False, null=False, verbose_name=_('Temperature spec'),
        max_digits=4, decimal_places=2)
