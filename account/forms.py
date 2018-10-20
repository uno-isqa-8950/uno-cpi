from django import forms
from home.models import User

class LoginForm(forms.Form):
    class Meta:
     model = User
     fields = ('email','password')

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)