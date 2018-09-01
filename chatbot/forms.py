from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'role')
        labels = {
            'role': _('Role'),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'role')
        labels = {
            'role': _('Role'),
        }
