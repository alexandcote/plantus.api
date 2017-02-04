from django.contrib import admin
from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email')
