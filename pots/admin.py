from django.contrib import admin

from pots.models import (
    Pot,
    TimeSerie,
    Action,
    Operation
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


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'label',)
    list_display_links = ('name',)


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('pot', 'action', 'created_at', 'completed_at',)
    list_filter = ('action', 'pot', 'pot__place')
    list_display_links = ('pot',)
