from rest_framework import viewsets, permissions, authentication

from hello_uptime.api.serializers import MonitorSerializer
from hello_uptime.models import Monitor


class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.SessionAuthentication,)

    def get_queryset(self):
        return Monitor.objects.filter(user=self.request.user).order_by('created_at')
