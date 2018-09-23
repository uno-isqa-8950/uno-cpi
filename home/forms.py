from django import forms
from .models import User
from django.forms import ModelForm
from partners.models import CampusPartner, University, CommunityPartner
from home.models import CampusPartnerContact, MissionArea
from projects.models import Project


class CampusPartnerForm(forms.ModelForm):
    class Meta:
        model = CampusPartner
        fields = ('campusPartnerName',)


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
        fields = ('college', 'department', 'name')


class CampusPartnerContactForm(forms.ModelForm):
    class Meta:
        model = CampusPartnerContact
        fields = ('first_name', 'last_name', 'email_id')


class ProjectForm(forms.ModelForm):
    mission = forms.ModelChoiceField(queryset=MissionArea.objects.all(), to_field_name="mission")
    communityPartnerName = forms.ModelChoiceField(queryset=CommunityPartner.objects.all(),
                                                  to_field_name="communityPartnerName")
    campusPartnerName = forms.ModelChoiceField(queryset=CampusPartner.objects.all(), to_field_name="campusPartnerName")

    class Meta:
        model = Project
        fields = '__all__'




