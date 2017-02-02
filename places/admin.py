from django.contrib import admin

# Register your models here.
from places.models import Place


class PlaceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Place, PlaceAdmin)