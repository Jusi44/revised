# users/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile

# users/forms.py

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['notify_email', 'age', 'sex', 'height', 'weight']



