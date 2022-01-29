from django.contrib import admin

from accounts.models import SystemUser


class SystemUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)


admin.site.register(SystemUser, SystemUserAdmin)
