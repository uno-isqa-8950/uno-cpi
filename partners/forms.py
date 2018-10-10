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
            raise forms.ValidationError("Please use university email ex: yourname@unomaha.edu ")
        return data

