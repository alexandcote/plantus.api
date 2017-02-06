from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    list_display = ('__str__', 'email')
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups',
                       'user_permissions')}),
        (_('Important dates'), {
            'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(User, CustomUserAdmin)

