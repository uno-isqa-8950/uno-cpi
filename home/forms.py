from django import forms
from .models import User
from partners.models import CampusPartner, University
from home.models import CampusPartnerContact
from django.utils.translation import ugettext_lazy as _

class CampusPartnerForm(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('campus_partner_name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ('name', 'college','department')
        labels = {
            'name': _('University Name'),
        }
        UNIV_CHOICES = (
            ('UNO', 'University of Nebraska'),
        )
        coll_choices = (
            ('SOE', 'School of Engineering'),
        )
        widgets = {
            'name': forms.Select(choices=UNIV_CHOICES,attrs={'class': 'form-control'}),
            'college': forms.Select(choices=coll_choices,attrs={'class': 'form-control'}),
        }


class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerContact
        fields = ('first_name','last_name', 'email_id')
