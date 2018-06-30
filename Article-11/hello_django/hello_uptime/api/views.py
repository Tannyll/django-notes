from rest_framework import viewsets, permissions

from hello_uptime.api.serializers import MonitorSerializer
from hello_uptime.models import Monitor


class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Monitor.objects.filter(user=self.request.user)
