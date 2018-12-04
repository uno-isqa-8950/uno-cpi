from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, TextInput
from django.db.transaction import commit
import re
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
# importing models in forms.py
from university.models import *
from .models import User
from partners.models import CampusPartner, CommunityPartner,CommunityPartnerUser,CommunityPartnerMission, \
    CommunityType, CampusPartnerUser
from home.models import Contact, MissionArea, HouseholdIncome
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, \
    ProjectCommunityPartner, ProjectMission, AcademicYear


class CampusPartnerUserForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerUser
        fields = ('campus_partner',)
        labels = {
            'campus_partner':('Campus Partner')
        }

        campus_partner = forms.ModelChoiceField(
        queryset=CampusPartner.objects.order_by().distinct('name'),
        label='Campus Partner Name', help_text='Please Register Your Organization if not found in list')
        #print(campus_partner)


class CommunityPartnerUserForm(forms.ModelForm):

    class Meta:
        model = CommunityPartnerUser
        fields = ('community_partner',)
        labels = {
            'community_partner': ('Community Partner')
        }
        community_partner = forms.ModelChoiceField(
        queryset=CommunityPartner.objects.order_by().distinct('name'),
                                 label='Community Partner Name',help_text='Please Register your Organization if not found in list')


class CampususerForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               help_text='Atleast 8 characters having 1 digit and 1 special character')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                help_text='Atleast 8 characters having 1 digit and 1 special character')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First Name should not have Special Characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last Name should not have Special Characters")
        return lastname

    def clean_email(self):
        email = self.cleaned_data['email']
        if "edu" != email.split("@")[1].split('.')[1]:
            raise forms.ValidationError("Please use .edu email ")
        return email

    def clean_password2(self):
        pas = self.cleaned_data['password']
        cd = self.cleaned_data['password2']
        MIN_LENGTH = 8
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if pas and cd:
            if pas != cd:
                raise forms.ValidationError('Passwords don\'t match.')
            else:
                if len(pas) < MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters" % MIN_LENGTH)
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")
                if pas.isalpha():
                    raise forms.ValidationError("Password should have atleast one digit")
                if not any(char in special_characters for char in pas):
                    raise forms.ValidationError("Password should have atleast one Special Character")


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

class CommunityuserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               help_text='Atleast 8 characters having 1 digit and 1 special character')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                help_text='Atleast 8 characters having 1 digit and 1 special character')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First Name should not have Special Characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last Name should not have Special Characters")
        return lastname



    def clean_password2(self):
        pas = self.cleaned_data['password']
        cd = self.cleaned_data['password2']
        MIN_LENGTH = 8
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if pas and cd:
            if pas != cd:
                raise forms.ValidationError('Passwords don\'t match.')
            else:
                if len(pas) < MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters" % MIN_LENGTH)
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")
                if pas.isalpha():
                    raise forms.ValidationError("Password should have atleast one digit")
                if not any(char in special_characters for char in pas):
                    raise forms.ValidationError("Password should have atleast one Special Character")


class userUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email' )

        labels = {

            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'email': ('Email ID')
        }

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First Name should not have Special Characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last Name should not have Special Characters")
        return lastname

    def clean_email(self):
        email = self.cleaned_data['email']
        if "edu" != email.split("@")[1].split('.')[1]:
            raise forms.ValidationError("Please use .edu email ")
        return email


class CommunityPartnerForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email' )
        help_texts = {

            'email': None,
        }

        labels = {

            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'email': ('Email ID')
        }

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First Name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First Name should not have Special Characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last Name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last Name should not have Special Characters")
        return lastname

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



class UploadProjectForm(forms.ModelForm):
    engagement_type = forms.ModelChoiceField(queryset=EngagementType.objects.all(), to_field_name="name")
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), to_field_name="name")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), to_field_name="name")
    academic_year = forms.ModelChoiceField(queryset=AcademicYear.objects.all(), to_field_name="academic_year")

    class Meta:
        model = Project
        fields = ('project_name', 'engagement_type', 'activity_type', 'facilitator', 'description', 'semester',
                  'academic_year', 'total_uno_students', 'total_uno_hours', 'total_k12_students', 'total_k12_hours',
                  'total_uno_faculty', 'total_other_community_members', 'other_details', 'outcomes',
                  'total_economic_impact', 'status', 'longitude', 'latitude', 'address_line1', 'city', 'state','county',
                  'legislative_district','median_household_income',)


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


class UploadCommunityMissionForm(forms.ModelForm):
    mission_area = forms.ModelChoiceField(queryset=MissionArea.objects.all(), to_field_name="mission_name")
    community_partner = forms.ModelChoiceField(queryset=CommunityPartner.objects.all(),
                                               to_field_name="name")

    class Meta:
        model = CommunityPartnerMission
        fields = '__all__'
        mission_choices = (
            ('Primary', 'Primary'),
            ('Other', 'Other'),
        )
        mission_type = forms.ChoiceField(widget=forms.Select(choices=mission_choices))


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


class UploadIncome(ModelForm):

    class Meta:
        model = HouseholdIncome
        fields = '__all__'


class CampusPartnerAvatar(ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)

        labels = {
            'avatar': ('Profile Photo'),
                 }
        widgets ={
            'avatar': forms.FileInput({'placeholder': 'Upload pic'}),

        }

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # # validate dimensions
            max_width = max_height = 600
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (2 * 1024 *1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 2mb.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    topic = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].widget.attrs['placeholder'] = "Full Name"
        self.fields['contact_email'].widget.attrs['placeholder'] = "Your Email"
        #self.fields['topic'].label = "Subject"
        self.fields['topic'].widget.attrs['placeholder'] = 'Subject'
        #self.fields['content'].label = "Message"
        self.fields['content'].widget.attrs['placeholder'] = 'Message'