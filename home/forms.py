from django import forms
from django.db.transaction import commit
import re

from university.models import *
from .models import User
from django.contrib.auth.forms import UserCreationForm
from partners.models import CampusPartner, CommunityPartner,CommunityPartnerUser,CommunityPartnerMission, \
    CommunityType, CampusPartnerUser
from home.models import Contact, MissionArea
from django.utils.translation import ugettext_lazy as _
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission
from django.forms import ModelForm, TextInput



EMAIL_REGEX1 = r'\w+@\unomaha.edu' # If you only want to allow unomaha.edu.


class CampusPartnerUserForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerUser
        fields = ('campus_partner',)

        campus_partner = forms.ModelChoiceField(
        queryset=CampusPartner.objects.order_by().distinct('name'),
        label='Campus Partner Name', help_text='Please Register Your Organization if not found in list')
        #print(campus_partner)

    def clean_email_id (self):
        data = self.cleaned_data.get('email_id')
        domain = data.split('@')[1]
        domain_list = ["unomaha.edu" ]
        if domain not in domain_list:
            raise forms.ValidationError("Please use university email ex: yourname@unomaha.edu ")
        return data

class CommunityPartnerUserForm(forms.ModelForm):

    class Meta:
        model = CommunityPartnerUser
        fields = ('community_partner',)

        community_partner = forms.ModelChoiceField(
        queryset=CommunityPartner.objects.order_by().distinct('name'),
                                 label='Community Partner Name',help_text='Please Register your Organization if not found in list')





class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email' )
        help_texts = {
            'username': None,
            'email': None,
        }

        labels = {
            'username': ('User Name'),
            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'email': ('Email ID')
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']




class UploadProjectForm(forms.ModelForm):
    engagement_type = forms.ModelChoiceField(queryset=EngagementType.objects.all(), to_field_name="name")
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), to_field_name="name")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), to_field_name="name")

    class Meta:
        model = Project
        fields = ('project_name', 'engagement_type', 'activity_type', 'facilitator', 'description', 'semester',
                  'total_uno_students', 'total_uno_hours', 'total_k12_students', 'total_k12_hours', 'total_uno_faculty',
                  'total_other_community_members', 'other_details', 'outcomes', 'total_economic_impact', 'status')


class UploadProjectCampusForm(forms.ModelForm):
    project_name = forms.ModelChoiceField(queryset=Project.objects.all(), to_field_name="project_name")
    campus_partner = forms.ModelChoiceField(queryset=CampusPartner.objects.all(), to_field_name="name")

    class Meta:
        model = ProjectCampusPartner
        fields = ('project_name', 'campus_partner')


class UploadProjectCommunityForm(forms.ModelForm):
    project_name = forms.ModelChoiceField(queryset=Project.objects.all(), to_field_name="project_name")
    community_partner = forms.ModelChoiceField(queryset=CommunityPartner.objects.all(), to_field_name="name")

    class Meta:
        model = ProjectCommunityPartner
        fields = ('project_name', 'community_partner')


class UploadProjectMissionForm(forms.ModelForm):
    project_name = forms.ModelChoiceField(queryset=Project.objects.all(), to_field_name="project_name")
    mission = forms.ModelChoiceField(queryset=MissionArea.objects.all(), to_field_name="mission_name")

    class Meta:
        model = ProjectMission
        fields = '__all__'
        mission_choices = (
            ('Primary', 'Primary'),
            ('Secondary', 'Secondary'),
            ('Other', 'Other'),
        )
        mission_type = forms.ChoiceField(widget=forms.Select(choices=mission_choices))


class UploadCommunityForm(forms.ModelForm):
    community_type = forms.ModelChoiceField(queryset=CommunityType.objects.all(), to_field_name="community_type")

    class Meta:
        model = CommunityPartner
        fields = '__all__'
        TRUE_FALSE_CHOICES = (
            ('True', 'Yes'),
            ('False', 'No'),
        )
        weitz_cec_part = forms.ChoiceField(widget=forms.Select(choices=TRUE_FALSE_CHOICES))


class UploadCampusForm(forms.ModelForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), to_field_name="name")
    education_system = forms.ModelChoiceField(queryset=EducationSystem.objects.all(), to_field_name="name")
    college_name = forms.ModelChoiceField(queryset=College.objects.all(), to_field_name="college_name")

    class Meta:
        model = CampusPartner
        fields = '__all__'
        TRUE_FALSE_CHOICES = (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )
        weitz_cec_part = forms.ChoiceField(widget=forms.Select(choices=TRUE_FALSE_CHOICES))


class UploadCollege(ModelForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), to_field_name="name")

    class Meta:
        model = College
        fields = ('college_name', 'university')


class UploadDepartment(ModelForm):
    college_name = forms.ModelChoiceField(queryset=College.objects.all(), to_field_name="college_name")

    class Meta:
        model = Department
        fields = '__all__'



