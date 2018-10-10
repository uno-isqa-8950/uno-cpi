from django import forms
from django.forms import ModelForm
from home.models import Contact
from partners.models import *
from django.forms import modelformset_factory
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import inlineformset_factory


class CampusPartnerForm(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('name', 'education_system','university', 'college_name', 'department',)

        labels= {
            'name': ('Campus Partner Name'),
             }


class CampusPartnerFormProfile(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('name', 'education_system','university', 'college_name', 'department',)

        labels= {
            'name': ('Campus Partner Name'),
             }
        # widgets = {
        #     'name': {'disable': True}
        # }


class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model= Contact
        fields =('first_name','last_name','work_phone','cell_phone','email_id','contact_type',)

        labels = {
            'first_name': ('Contact First Name'),
            'last_name': ('Contact Last Name'),
            'work_phone': ('Contact Work Phone#'),
            'cell_phone': ('Contact Cell Phone#'),
            'email_id': ('Contact Email Id'),

        }

        widgets = {'work_phone': forms.TextInput({'placeholder': '5714200002'}),
                   'cell_phone': forms.TextInput({'placeholder': '5714200002'}),
                   'email_id': forms.TextInput({'placeholder': 'abc@unomaha.edu'}),
                   }


    def clean_email_id (self):
        data = self.cleaned_data.get('email_id')
        domain = data.split('@')[1]
        domain_list = ["unomaha.edu" ]
        if domain not in domain_list:
            raise forms.ValidationError("Please use university email (@unomaha.edu)")
        return data


class CommunityPartnerForm(forms.ModelForm):

    class Meta:
        model = CommunityPartner
        fields = ('name', 'website_url', 'community_type', 'k12_level', 'address_line1', 'address_line2', 'county',
                  'city', 'state', 'zip')
        widgets = {'name': forms.TextInput({'placeholder': 'Community Partner Name'}),
                   'website_url': forms.TextInput({'placeholder': 'https://www.unomaha.edu'}),
                   'k12_level' :forms.TextInput({'placeholder': 'If your community type is K12, Please provide the k12-level'}),
                   }
    # def clean_website_url(self):
    #    data = self.cleaned_data.get('website_url')
    #    if  not  data.startswith ('https://'):
    #     raise forms.ValidationError('Url should start from "https://".')
    #    return data


class CommunityContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'work_phone',
                  'cell_phone',
                  'email_id',
                  'contact_type')
        widgets = {'work_phone': forms.TextInput({'placeholder': '5714200002'}),
                   'cell_phone': forms.TextInput({'placeholder': '5714200002'}),
                  }


class CommunityMissionForm(ModelForm):

    mission_choices = (
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Other', 'Other'),
    )

    class Meta:
        model = CommunityPartnerMission
        fields = ('mission_type' , 'mission_area')


