from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from home.models import Contact, User, MissionArea
from partners.models import *
from university.models import *
from django.forms import modelformset_factory
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import inlineformset_factory


class CampusPartnerForm(forms.ModelForm):
    # department = forms.ModelChoiceField(queryset=Department.objects, empty_label='Select Department')
    class Meta:
        model = CampusPartner
        fields = ('name', 'college_name',)
        exclude = ('department', 'education_system','university',)

        labels= {
            'name': ('Campus Partner Name'),
            'college_name': ('College or Main Unit')
             }

    def __init__(self, *args, **kwargs):
        super(CampusPartnerForm, self).__init__(*args, **kwargs)
        self.fields['college_name'].empty_label = "Select College"


class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model= Contact
        fields =('first_name','last_name','work_phone','cell_phone','email_id','contact_type',)

        labels = {
            'first_name': ('Contact First Name'),
            'last_name': ('Contact Last Name'),
            'work_phone': ('Work Phone'),
            'cell_phone': ('Cell Phone'),
            'email_id': ('Contact Email'),
            'contact_type':('Contact Type'),
        }
        widgets = {
                   'email_id': forms.TextInput({'placeholder': '@abc.edu'}),
                   }
    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First name should not have special characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last name should not have special characters")
        return lastname

    def clean_work_phone(self):
        workphone = self.cleaned_data['work_phone']
        if any(char.isalpha() for char in workphone):
            raise forms.ValidationError("Work Phone cannot have alphabets")
        return workphone

  #  def clean_cell_phone(self):
   #     cellphone = self.cleaned_data['cell_phone']
    #    if any(char.isalpha() for char in cellphone):
     #       raise forms.ValidationError("Cell Phone cannot have alphabets")
      #  return cellphone

    def clean_email_id(self):
        email = self.cleaned_data['email_id']
        sufix = ".edu"
        if not email.endswith(sufix):
            raise forms.ValidationError("Please use your campus email (.edu) for the registration of a Campus Partner.")
        return email

class CommunityPartnerForm(forms.ModelForm):
    website_url = forms.URLField(max_length=200,label='Your Website', required=False)
    address_line1 = forms.CharField(max_length=200,label='Address', required=True)
    class Meta:
        model = CommunityPartner
        fields = ('name', 'website_url', 'community_type', 'k12_level', 'address_line1', 'city','state',
                   'zip','county','country')
        labels = {
            'name': ('Community Partner Organization'),
            # 'website_url': ('Website'),
            'community_type': ('Community Type'),
            'k12_level':('K12 Level'),
            'city': ('City'),
            'state': ('State'),
            'zip':('Zip Code'),
            'county':('County'),
            'country':('Country'),

        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if CommunityPartner.objects.filter(name__icontains=name).exists():
            raise forms.ValidationError('Community partner with this Name already exists.')
        return name

    def clean_country(self):
            name = self.cleaned_data['country']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("Country cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("Country cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a Country Name")
            return name

    def clean_state(self):
            name = self.cleaned_data['state']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("State cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("State cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a State Name")
            return name

    def clean_city(self):
            name = self.cleaned_data['city']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("City cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("City cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a City Name")
            return name


    # def clean_zip(self):
    #     zip = self.cleaned_data['zip']
    #     if any(char.isalpha() for char in zip):
    #         raise forms.ValidationError("Zip cannot have alphabets")
    #     if len(zip) == 0:
    #         raise forms.ValidationError("Please enter a Zip Code")
    #     return zip

class CommunityPartnerUpdateForm(forms.ModelForm):
    website_url = forms.URLField(max_length=200,label='Your Website', required=False)
    address_line1 = forms.CharField(max_length=200,label='Address', required=True)
    class Meta:
        model = CommunityPartner
        fields = ('name', 'website_url', 'community_type', 'k12_level', 'address_line1', 'city','state',
                   'zip','country')
        labels = {
            'name': ('Community Partner Organization'),
            # 'website_url': ('Website'),
            'community_type': ('Community Type'),
            'k12_level':('K12 Level'),
            'city': ('City'),
            'state': ('State'),
            'zip':('Zip Code'),
            # 'county':('County'),
            'country':('Country'),

        }

    def clean_country(self):
            name = self.cleaned_data['country']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("Country cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("Country cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a Country Name")
            return name

    def clean_state(self):
            name = self.cleaned_data['state']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("State cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("State cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a State Name")
            return name

    def clean_city(self):
            name = self.cleaned_data['city']
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            if any(char.isdigit() for char in name):
                raise forms.ValidationError("City cannot have digits")
            if any(char in special_characters for char in name):
                raise forms.ValidationError("City cannot have digits")
            if len(name) == 0:
                raise forms.ValidationError("Please enter a City Name")
            return name


    # def clean_zip(self):
    #     zip = self.cleaned_data['zip']
    #     if any(char.isalpha() for char in zip):
    #         raise forms.ValidationError("Zip cannot have alphabets")
    #     if len(zip) == 0:
    #         raise forms.ValidationError("Please enter a Zip Code")
    #     return zip

class CommunityContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'work_phone',
                  'cell_phone',
                  'email_id',
                  'contact_type')
        labels = {
            'email_id': ('Contact Email'),
            'contact_type': ('Contact Type'),
            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'work_phone': ('Work Phone'),
            'cell_phone': ('Cell Phone')
        }


    def validateEmail(email_id):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email_id)
            return True
        except ValidationError:
            return False

    def clean_first_name(self):
        firstname = self.cleaned_data['first_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError("First name cannot have digits")
        if any(char in special_characters for char in firstname):
            raise forms.ValidationError("First name should not have special characters")
        return firstname

    def clean_last_name(self):
        lastname = self.cleaned_data['last_name']
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError("Last name cannot have digits")
        if any(char in special_characters for char in lastname):
            raise forms.ValidationError("Last name should not have special characters")
        return lastname

    def clean_work_phone(self):
        workphone = self.cleaned_data['work_phone']
        if any(char.isalpha() for char in workphone):
            raise forms.ValidationError("Work Phone cannot have alphabets")
        return workphone

    #def clean_cell_phone(self):
     #   cellphone = self.cleaned_data['cell_phone']
     #   if any(char.isalpha() for char in cellphone):
     #       raise forms.ValidationError("Cell Phone cannot have alphabets")
     #   return cellphone

class CommunityMissionForm(ModelForm):

    mission_choices = (
        ('Primary', 'Primary'),
        ('Other', 'Other'),
    )

    mission_area = forms.ModelChoiceField(queryset=MissionArea.objects, label='Mission Area', empty_label='Select Mission Area')
    class Meta:
        model = CommunityPartnerMission
        fields = ('mission_type' , 'mission_area')
        labels = {
            'mission_type': ('Mission Type'),
            'mission_area': ('Mission Area'),
        }

class CommunityMissionFormset(forms.ModelForm):
    class Meta:
        model = CommunityPartnerMission
        fields = ( 'mission_area',)
        labels = {
            'mission_area': ('Mission Area'),
                    }


class PrimaryCommunityMissionFormset(forms.ModelForm):
    class Meta:
        model = CommunityPartnerMission
        fields = ( 'mission_area',)
        labels = {
            'mission_area': ('Mission Area'),
        }

class CampusPartnerAddForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerUser
        fields = ('campus_partner',)
        labels = {'campus_partner': ('Existing Campus Partners')}

    def __init__(self, *args, **kwargs):
        super(CampusPartnerAddForm, self).__init__(*args, **kwargs)

class CommunityPartnerAddForm(forms.ModelForm):

    class Meta:
        model = CommunityPartnerUser
        fields = ('community_partner',)
        labels = {'community_partner': ('Existing Community Partners')}

    def __init__(self, *args, **kwargs):
        super(CommunityPartnerAddForm, self).__init__(*args, **kwargs)


