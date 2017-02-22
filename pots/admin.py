from django.contrib import admin

from pots.models import (
    Pot,
    TimeSerie
)


@admin.register(Pot)
class PotAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'plant')
    list_filter = ('place__users',)


@admin.register(TimeSerie)
class TimeSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'pot', 'date',)
    list_filter = ('pot', 'pot__place__users',)
    list_display_links = ('id', 'pot',)
