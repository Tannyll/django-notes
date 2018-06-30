from rest_framework import serializers

from hello_uptime.models import Monitor


class MonitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monitor
        fields = ('url', 'monitor_url', 'interval', 'status', 'is_active', 'checked_at', 'created_at')
