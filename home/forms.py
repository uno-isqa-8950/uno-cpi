from django import forms
from .models import User
from partners.models import CampusPartner, University, CommunityPartner
from home.models import CampusPartnerContact, Contact
from django.utils.translation import ugettext_lazy as _


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
        fields = ('campus_partner_name',)
       

    campus_partner_name = forms.ModelChoiceField(queryset=CampusPartner.objects.order_by().distinct('campus_partner_name'),
                                      label='Campus Partner Name', help_text= 'Please Register Your Organization if not found in list')


class CampusPartnerForm(forms.ModelForm):

    class Meta:
        model = CampusPartner
        fields = ('campus_partner_name',)


class CommunityPartnerUserForm(forms.ModelForm):

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s</p>%(field)s%(help_text)s',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)

    class Meta:
        model = CommunityPartner
        fields = ('CommunityPartnerName',)

    name = forms.ModelChoiceField(queryset=CommunityPartner.objects.order_by().distinct('CommunityPartnerName')
                                  ,label='Community Partner Name',help_text='Please Register your Organization if not found in list')


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s</p>%(field)s%(help_text)s',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)



    # def as_p(self):
    #     "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
    #     return self._html_output(
    #         normal_row='%(label)s%(errors)s%(field)s%(help_text)s',
    #         error_row='%s',
    #         row_ender=' ',
    #         help_text_html='<br /><span class="helptext">%s</span>',
    #         errors_on_separate_row=False)
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


class UniversityForm(forms.ModelForm):
    # Comment commit
    class Meta:
        model = University
        fields = ('name', )
        labels = {
            'name': _('University Name'),
        }

        uni_choices = (("0", "Select University"), )
        # coll_choices = (("0", "Select college"), )
        # dep_choices = (("0", "Select Department"), )

        widgets = {
            'name': forms.Select(choices=uni_choices, ),
            # 'college': forms.Select(choices=coll_choices, ),
            # 'department': forms.Select(choices=dep_choices, ),
        }

    # def __init__(self, *args, **kwargs):
    #     super(UniversityForm, self).__init__(*args, **kwargs)
    #     # self.fields['name'].widget.choices = (
    #     #     (univ.get('id'), univ.get("name")) 
    #     #     for univ in University.objects.all().values('name', 'id').distinct('name')
    #     # )
    #     self.fields['college'].widget.attrs['disabled'] = True
    #     self.fields['department'].widget.attrs['disabled'] = True


class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerContact
        fields = ('first_name','last_name', 'email_id')

class CommunityPartnerForm(forms.ModelForm):
    class Meta:
        model = CommunityPartner
        fields = ('CommunityPartnerName', 'website_url', 'communitytype', 'k12_level', 'primary_mission', 'secondary_mission',
                  'other', 'address_line1', 'address_line2', 'country', 'city', 'state', 'Zip')


class CommunityContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'workphone',
                  'cellphone',
                  'contact_type',
                  'email_id')