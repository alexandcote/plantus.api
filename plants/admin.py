from django.contrib import admin

from plants.models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'humidity_spec', 'luminosity_spec', 'temperature_spec')
