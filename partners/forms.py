from django import forms
from django.forms import ModelForm
from home.models import Contact
from partners.models import CampusPartner
from django.forms import modelformset_factory
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import inlineformset_factory


class CampusPartnerForm(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('name', 'education_system','university', 'college', 'department',)

        labels= {
            'name': ('Campus Partner Name'),
             }


class CampusPartnerFormProfile(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('name', 'education_system','university', 'college', 'department',)

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

        error_messages = {
            'name': {'required': ("Campus Partner Name is required")},
            'cellphone': {'max_length': ("Phone number is not valid"),}
            },
        help_texts= {'email_id' :'(ex: abc@unomaha.edu)'}



        def clean_email_id (self):
            data = self.cleaned_data.get('email_id')
            domain = data.split('@')[1]
            domain_list = ["unomaha.edu" ]
            if domain not in domain_list:
                raise forms.ValidationError("Please enter an Email Address with a valid domain")
            return data


