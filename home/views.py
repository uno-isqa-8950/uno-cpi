from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from partners.models import CampusPartnerUser
from .forms import  CampusPartnerForm, UniversityForm, CampusPartnerContactForm, UserForm, CommunityPartnerForm, CommunityTypeForm, CommunityPartnerMissionForm, CommunityContactForm, CommunityAddressForm
from django.urls import reverse


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})

  
def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})

  
def registerCampusPartnerUser(request):
    campus_partner_form = CampusPartnerForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        campus_partner_form = CampusPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            CampusPartnerUser(campuspartner=CampusPartner.objects.filter(campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0],user=new_user)
            return render(request,'home/register_done.html',)
    return render(request,
                  'home/campus_partner_user_register.html',
                  {'campus_partner_form': campus_partner_form, 'user_form': user_form})



def registerCampusPartner(request):
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)
        university_form = UniversityForm(request.POST)
        contact_form = CampusPartnerContactForm(request.POST)
        if campus_partner_form.is_valid() and university_form.is_valid() and contact_form.is_valid():
            # Create a new user object but avoid saving it yet
            University =  university_form.save()
            cp = CampusPartner(campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'], department_id=University)
            cp.save()
            cpc =  CampusPartnerContact(first_name=contact_form.cleaned_data['first_name'],last_name=contact_form.cleaned_data['last_name'], email_id = contact_form.cleaned_data['email_id'], partner_name =cp)
            cpc.save()
            return render(request,'home/register_done.html',)
    else:
        campus_partner_form = CampusPartnerForm()
        university_form = UniversityForm()
        contact_form = CampusPartnerContactForm()
    return render(request,
                  'home/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'university_form': university_form, 'contact_form': contact_form})


def registerCommunityPartner(request):
    if request.method == 'POST':
        community_partner_form = CommunityPartnerForm(request.POST)
        community_partner_mission_form = CommunityPartnerMissionForm(request.POST)
        community_type_form = CommunityTypeForm(request.POST)
        community_contact_form = CommunityContactForm(request.POST)
        community_address_form = CommunityAddressForm(request.POST)

        if community_partner_form.is_valid() and community_partner_mission_form.is_valid() and community_type_form.is_valid() and community_contact_form.is_valid() and community_address_form.is_valid() :
            # Create a new user object but avoid saving it yet
            commpart = CommunityPartner(name=CommunityPartnerForm.cleaned_data['name'], website_url=CommunityPartnerForm.cleaned_data['website_url'],k12_level=CommunityPartnerForm.cleaned_data['k12_level'])
            commpart.save()
            commpartm = CommunityPartnerMission(mission_type=CommunityPartnerMissionForm.cleaned_data['mission_type'])
            commpartm.save()
            commpartt = CommunityType(community_type=CommunityType.cleaned_data['community_type'])
            commpartt.save()
            commpartc =  CampusPartnerContact(first_name=CommunityContactForm.cleaned_data['first_name'],last_name=CommunityContactForm.cleaned_data['last_name'], email_id = CommunityContactForm.cleaned_data['email_id'],
                                              workphone=CommunityContactForm.cleaned_data['workphone'],cellphone=CommunityContactForm.cleaned_data['cellphone'])
            commpartc.save()
            comparta = Address(address_line1=CommunityAddressForm.cleaned_data['address_line1'],address_line2=CommunityAddressForm.cleaned_data['address_line2'],country=CommunityAddressForm.cleaned_data['country'],
                               city=CommunityAddressForm.cleaned_data['city'],state=CommunityAddressForm.cleaned_data['state'],Zip=CommunityAddressForm.cleaned_data['Zip'])
            comparta.save()
            return render(request,'home/community_partner_register_done.html',)
    else:
        community_partner_form = CommunityPartnerForm()
        community_type_form = CommunityTypeForm()
        community_partner_mission_form = CommunityPartnerMissionForm()
        community_contact_form = CommunityContactForm()
        community_address_form = CommunityAddressForm()

    return render(request,
                  'home/community_partner_register.html',
                  {'community_partner_form': community_partner_form, 'community_type_form': community_type_form,
                   'community_partner_mission_form': community_partner_mission_form,'community_contact_form': community_contact_form, 'community_address_form': community_address_form   })