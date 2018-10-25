from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import CustomUser
import datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'roomnumber', 'checkindatetime', 'checkoutdatetime')
        labels = {
            # 'role': _('Role'),
            'roomnumber': _('Room No'),
            'email': _('Email'),
            'checkindatetime': _('Checkin Date&Time'),
            'checkoutdatetime': _('Checkout Date&Time')
        }
        checkindatetime = forms.DateTimeField(
            input_formats=('%Y-%m-%d %H:%M:%S')
        )  
        checkoutdatetime = forms.DateTimeField(
            input_formats=('%Y-%m-%d %H:%M:%S')
        )      
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # fields = ('username', 'email', 'role', 'roomnumber', 'checkindatetime', 'checkoutdatetime')
        fields = ('username', 'email', 'roomnumber', 'checkindatetime', 'checkoutdatetime')
        labels = {
            # 'role': _('Role'),
            'roomnumber': _('Room No'),
            'email': _('Email'),
            'checkindatetime': _('Checkin Date&Time'),
            'checkoutdatetime': _('Checkout Date&Time')
        }
