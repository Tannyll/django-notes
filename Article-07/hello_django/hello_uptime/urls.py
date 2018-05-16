from django.urls import path
from hello_uptime.views import UptimeDashboardView

app_name = 'uptime'

urlpatterns = [
    path('', view=UptimeDashboardView.as_view(), name='dashboard'),
]
