from django.contrib import admin

from userroles.models import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'verbose_name']