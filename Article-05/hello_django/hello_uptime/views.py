from django.urls import reverse_lazy
from extra_views import ModelFormSetView

from hello_uptime.models import Monitor
from hello_uptime.utils import USER_MONITOR_LIMIT


class UptimeDashboardView(ModelFormSetView):
    fields = ('url', 'interval', 'is_active')
    model = Monitor
    success_url = reverse_lazy('uptime:dashboard')
    template_name = 'uptime/dashboard.html'

    def get_queryset(self):
        return Monitor.objects.order_by('id')

    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        kwargs.update({
            'extra': USER_MONITOR_LIMIT,
            'max_num': USER_MONITOR_LIMIT,
        })
        return kwargs

    def formset_valid(self, formset):
        formset.save()
        return super().formset_valid(formset)
