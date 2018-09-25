from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from partners.models import CampusPartnerUser,CommunityPartnerUser,CampusPartner,CommunityPartner
from .forms import  CampusPartnerForm, UniversityForm, CampusPartnerContactForm, UserForm, CommunityPartnerForm, CommunityContactForm
from django.urls import reverse


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})


def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})



def signup(request):
    return render(request, 'home/registration/signuporganization.html', {'signup': signup})


def signupuser(request):
    return render(request, 'home/registration/signupuser.html', {'signupuser': signupuser})


def registerCampusPartnerUser(request):
    campus_partner_user_form = CampusPartnerUserForm()

    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)
        #community_partner_form = CommunityPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_user_form.is_valid():
                #and community_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # cpu = CampusPartnerUser(campuspartner=CampusPartner.objects.filter(
            #         campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0], user=new_user)
            cpu = CampusPartnerUser(campuspartner=campus_partner_user_form.cleaned_data['campus_partner_name'], user=new_user)
            cpu.save()

            return render(request,'home/register_done.html',)
    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  { 'user_form': user_form,'campus_partner_user_form': campus_partner_user_form})


def registerCommunityPartnerUser(request):

    community_partner_user_form = CommunityPartnerUserForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        #campus_partner_form = CampusPartnerForm(request.POST)
        community_partner_user_form = CommunityPartnerUserForm(request.POST)
        if user_form.is_valid() and community_partner_user_form.is_valid():
               # and campus_partner_form.is_valid()
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # cpu = CommunityPartnerUser(communitypartner=CommunityPartner.objects.filter(
            #        name=community_partner_form.cleaned_data['name'])[0], user=new_user)
            cpu = CommunityPartnerUser(communitypartner=community_partner_user_form.cleaned_data['name'], user=new_user)
            cpu.save()
            return render(request,'home/register_done.html',)
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  { 'user_form': user_form,'community_partner_user_form': community_partner_user_form})


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
            cpc = CampusPartnerContact(first_name=contact_form.cleaned_data['first_name'],last_name=contact_form.cleaned_data['last_name'], email_id = contact_form.cleaned_data['email_id'], partner_name =cp)
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
        community_partner_contact_form = CommunityContactForm(request.POST)

        if community_partner_form.is_valid() and community_partner_contact_form.is_valid():
            community_partner_form.save()
            community_partner_contact_form.save()

            return render(request,'home/community_partner_register_done.html',)
    else:
        community_partner_form = CommunityPartnerForm()
        community_partner_contact_form = CommunityContactForm()

    return render(request,
                  'home/community_partner_register.html',
                  {'community_partner_form': community_partner_form,'community_partner_contact_form':community_partner_contact_form},)