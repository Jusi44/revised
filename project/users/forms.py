from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    username = forms.CharField(max_length=150, required=True, label="Username")
    verification_code = forms.CharField(required=False, label="Email Verification Code")

    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False, widget=forms.Select())

    class Meta:
        model = Profile
        fields = ['notify_email', 'age', 'sex', 'height', 'weight']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            profile.user.username = self.cleaned_data['username']
            profile.user.save()
        return profile
