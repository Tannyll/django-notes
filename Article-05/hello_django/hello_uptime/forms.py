from django import forms

from hello_uptime.models import Monitor


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ('url', 'interval', 'is_active')
