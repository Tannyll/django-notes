from django.contrib import admin

from hello_uptime.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('url', 'interval', 'status', 'checked_at', 'created_at', 'is_active')
    list_filter = ('is_active', 'status', 'interval', 'checked_at')
    date_hierarchy = 'created_at'
    search_fields = ('url',)
