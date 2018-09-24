from django import forms
from .models import User
from partners.models import CampusPartner, University, CommunityPartner
from home.models import CampusPartnerContact
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class CampusPartnerForm(forms.ModelForm):
    campus_partner_name = forms.CharField(label='Campus Partner Name')
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


class CommunityPartnerForm(forms.ModelForm):
    name = forms.CharField(label='Community Partner Name')
    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s</p> %(field)s%(help_text)s',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)
    # communityPartners = forms.ModelMultipleChoiceField(
    #     queryset=CommunityPartner.objects.all().values('name').distinct(),
    #     #widget=forms.Select(),
    #     required = True,
    #     label = 'Community Partner',
    #
    # )

    class Meta:
        model = CommunityPartner
        fields = ('name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
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

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UniversityForm(forms.ModelForm):
    # Comment commit
    class Meta:
        model = University
        fields = ('name', 'college','department')
        labels = {
            'name': _('University Name'),
        }

        uni_choices = (("0", "Select University"), )
        coll_choices = (("0", "Select college"), )
        dep_choices = (("0", "Select Department"), )

        widgets = {
            'name': forms.Select(choices=uni_choices, ),
            'college': forms.Select(choices=coll_choices, ),
            'department': forms.Select(choices=dep_choices, ),
        }

    def __init__(self, *args, **kwargs):
        super(UniversityForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.choices = (
        #     (univ.get('id'), univ.get("name")) 
        #     for univ in University.objects.all().values('name', 'id').distinct('name')
        # )
        self.fields['college'].widget.attrs['disabled'] = True
        self.fields['department'].widget.attrs['disabled'] = True


class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerContact
        fields = ('first_name','last_name', 'email_id')
