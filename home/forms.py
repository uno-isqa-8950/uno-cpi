from django import forms
from .models import User
from partners.models import CampusPartner, University, CommunityPartner, CommunityPartnerMission, CommunityType
from home.models import CampusPartnerContact, Contact, Address

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
        fields = ('college','department', 'name',)

class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerContact
        fields = ('first_name','last_name', 'email_id',)


class CommunityPartnerForm(forms.ModelForm):

    class Meta:
        model = CommunityPartner
        fields = (
            'name',
            'website_url',
            'k12_level',
        )

class CommunityTypeForm(forms.ModelForm):
    class Meta:
        model = CommunityType
        fields = (
            'community_type',
    )

class CommunityPartnerMissionForm(forms.ModelForm):
    class Meta:
        model= CommunityPartnerMission
        fields = ('mission_type',
              )



class CommunityContactForm(forms.ModelForm):
    class Meta:
        model =  Contact
        fields = ( 'first_name',
                   'last_name',
                   'workphone',
                   'cellphone',
                   'email_id',
        )

class CommunityAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'address_line1',
            'address_line2',
            'country',
            'city',
            'state',
            'Zip',
    )


