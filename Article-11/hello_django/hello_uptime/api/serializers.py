from django.template.defaultfilters import date
from rest_framework import serializers

from hello_uptime.models import Monitor


class MonitorSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    checked_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Monitor
        fields = ('id', 'status', 'status_display', 'checked_at_formatted')

    def get_checked_at_formatted(self, obj):
        return date(obj.checked_at, 'DATETIME_FORMAT')
