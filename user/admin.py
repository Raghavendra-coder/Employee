from django.contrib import admin
from .models import User, Leaves


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    fields = ('email', 'first_name', 'last_name', 'role', 'username', 'date_joined')
    readonly_fields = ('username', 'date_joined')


class LeaveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start', 'end', 'status', 'day_count')


admin.site.register(User, UserAdmin)
admin.site.register(Leaves, LeaveAdmin)
