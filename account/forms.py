from django import forms
from home.models import User, Password_Reset_Snippet
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

UserModel = get_user_model()
class LoginForm(forms.Form):
    class Meta:
     model = User
     fields = ('email','password')

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("Please enter a valid Email address.There is no user registered with the specified Email address.")
            self.add_error('email', msg)
        return email