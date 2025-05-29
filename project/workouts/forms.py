from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['time_hour', 'time_minute', 'days']
        widgets = {
            'days': forms.CheckboxSelectMultiple(),
        }
