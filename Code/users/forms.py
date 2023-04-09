from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

domain_validator = RegexValidator(
    regex='@(wm\.edu|email.wm\.edu)$',
    message='Domain not valid must be a WM school account',
    code='invalid_domain',
)
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(validators=[domain_validator])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1','password2']

