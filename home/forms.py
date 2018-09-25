from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from partners.models import CampusPartner, University, CommunityPartner
from home.models import CampusPartnerContact, MissionArea
from projects.models import Project, ProjectPartner
from django.forms import ModelForm


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


class CampusPartnerForm(forms.ModelForm):
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

    class Meta:
        model = University
        fields = ('college','department', 'name')

class CampusPartnerContactForm(forms.ModelForm):

    class Meta:
        model = CampusPartnerContact
        fields = ('first_name','last_name', 'email_id')


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
