from django.views.generic import FormView

from hello_uptime.forms import MonitorForm


class UptimeDashboardView(FormView):
    template_name = 'uptime/dashboard.html'
    form_class = MonitorForm

    def get_success_url(self):
        return reverse('uptime:dashboard')
