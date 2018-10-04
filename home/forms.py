from django import forms
from django.db.transaction import commit
import re
from .models import User
from django.contrib.auth.forms import UserCreationForm
from partners.models import CampusPartner, CommunityPartner
from university.models import *
from home.models import  Contact
from django.utils.translation import ugettext_lazy as _
from projects.models import Project
from django.forms import ModelForm



EMAIL_REGEX1 = r'\w+@\unomaha.edu' # If you only want to allow unomaha.edu.


class CampusPartnerUserForm(forms.ModelForm):

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s</p>%(field)s%(help_text)s',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)

    class Meta:
        model = CampusPartner
        fields = ('name',)

    name = forms.ModelChoiceField(
        queryset=CampusPartner.objects.order_by().distinct('name'),
        label='Campus Partner Name', help_text='Please Register Your Organization if not found in list')







class CommunityPartnerUserForm(forms.ModelForm):

    class Meta:
        model = CommunityPartner
        fields = ('name',)

    name = forms.ModelChoiceField(
        queryset=CommunityPartner.objects.order_by().distinct('name'),
                                 label='Community Partner Name',help_text='Please Register your Organization if not found in list')

#### This is where you check the user flag as true and then we can call the decorator
    def save(self):
        user = super().save(commit=False)
        user.is_campuspartner = True
        if commit:
            user.save()
        return user


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


class CommunityPartnerForm(forms.ModelForm):

    class Meta:
        model = CommunityPartner
        fields = ('name', 'website_url', 'community_type', 'k12_level', 'address_line1', 'address_line2', 'country', 'city', 'state', 'zip')

        widgets = {'name': forms.TextInput({'placeholder': 'Community Partner Name'}),
                   'website_url': forms.TextInput({'placeholder': 'https://www.unomaha.edu'}),
                   'k12_level' :forms.TextInput({'placeholder': 'If your community type is K12, Please provide the k12-level'}),


                   }
        def clean_website_url(self):
         data = self.cleaned_data.get('website_url')
         if  not  data.startswith ('https://'):
            raise forms.ValidationError('Url should start from "https://".')
         return data


class CommunityContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'work_phone',
                  'cell_phone',
                  'email_id',
                  'contact_type')
        widgets = {'work_phone': forms.TextInput({'placeholder': '571-420-0002'}),
                   'cell_phone': forms.TextInput({'placeholder': '571-420-0002'}),
                  }



class ProjectForm(forms.ModelForm):
    # mission_name = forms.ModelChoiceField(queryset=MissionArea.objects.all(), to_field_name="mission_name")
    # CommunityPartnerName = forms.ModelChoiceField(queryset=CommunityPartner.objects.all(),
    #                                               to_field_name="communityPartnerName")
    # campus_partner_name = forms.ModelChoiceField(queryset=CampusPartner.objects.all(),
    #                                              to_field_name="campus_partner_name")

    class Meta:
        model = Project
        fields = '__all__'

    # ProjectName = forms.ModelChoiceField(queryset=Project.objects.all(), to_field_name="ProjectName")
    #
    # class Meta:
    #     model = ProjectPartner
    #     fields = '__all__'


class CommunityForm(ModelForm):
    class Meta:
        model = CommunityPartner
        fields = '__all__'


class CampusForm(ModelForm):

    class Meta:
        model = CampusPartner
        fields = '__all__'
        TRUE_FALSE_CHOICES = (
            ('True', 'Yes'),
            ('False', 'No'),
        )
        weitz_cec_part = forms.ChoiceField(widget=forms.Select(choices=TRUE_FALSE_CHOICES))


