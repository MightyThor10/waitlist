from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import RegexValidator
from .models import StudentProfile

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

class StudentProfileForm(forms.ModelForm):
    ACADEMIC_STATUS_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    ]
    academic_status = forms.ChoiceField(choices=ACADEMIC_STATUS_CHOICES, required=False)

    class Meta:
        model = StudentProfile
        fields = ['preferred_name', 'academic_status', 'major']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
