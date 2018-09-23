from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from partners.models import CampusPartner, University, CommunityPartner
from home.models import CampusPartnerContact

class CampusPartnerUserCreationForm(forms.ModelForm):
     campusPartners = forms.ModelMultipleChoiceField(
        queryset=CampusPartner.objects.all().values('campus_partner_name').distinct(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Campus Partner',
      )
    # class Meta:
    #     model = CampusPartner
    #     fields = ('campus_partner_name',)

     class Meta(UserCreationForm.Meta):
        model = User


     def save(self):
        user = super().save(commit=False)
        user.is_campuspartner = True
        user.save()
        campuspartner = CampusPartner.objects.create(user=user)
        campuspartner.interests.add(*self.cleaned_data.get('campusPartners'))
        return user


class CommunityPartnerUserCreationForm(forms.ModelForm):
    communityPartners = forms.ModelMultipleChoiceField(
        queryset=CommunityPartner.objects.all().values('name').distinct(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label='Community Partner',
    )

    # class Meta:
    #     model = CampusPartner
    #     fields = ('campus_partner_name',)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):
        user = super().save(commit=False)
        user.is_communitypartner = True
        user.save()
        communitypartner = CampusPartner.objects.create(user=user)
        communitypartner.interests.add(*self.cleaned_data.get('communityPartners'))
        return user


class CommunityPartnerForm(forms.ModelForm):
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



class CampusPartnerForm(forms.ModelForm):

    # campusPartners= forms.ModelMultipleChoiceField(
    #     queryset=CampusPartner.objects.all().values('campus_partner_name').distinct(),
    #     required=True,
    #     label='Campus Partner',
    #
    # )

    class Meta:
        model = CampusPartner
        fields = ('campus_partner_name',)


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)


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
