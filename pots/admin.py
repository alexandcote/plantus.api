from django.contrib import admin

from pots.models import Pot


@admin.register(Pot)
class PotAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'plant')
    list_filter = ('place__users',)
