from .models import *
from university.models import *
from partners.models import CampusPartnerUser, CommunityPartnerUser, CampusPartner, CommunityPartner
from .forms import UserForm, CommunityPartnerForm, CommunityContactForm, CampusPartnerUserForm, \
    CommunityPartnerUserForm, ProjectForm, CommunityForm ,  CampusForm
from django.shortcuts import render
from django.urls import reverse
import csv
from collections import OrderedDict
from django.contrib import messages


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
        # community_partner_form = CommunityPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_user_form.is_valid():
            # and community_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # cpu = CampusPartnerUser(campuspartner=CampusPartner.objects.filter(
            #         campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0], user=new_user)
            cpu = CampusPartnerUser(campuspartner=campus_partner_user_form.cleaned_data['name'], user=new_user)
            cpu.save()

            return render(request, 'home/register_done.html', )
    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form})


def registerCommunityPartnerUser(request):
    community_partner_user_form = CommunityPartnerUserForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        # campus_partner_form = CampusPartnerForm(request.POST)
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
            return render(request, 'home/register_done.html', )
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form})







def registerCommunityPartner(request):
    if request.method == 'POST':
        community_partner_form = CommunityPartnerForm(request.POST)
        community_partner_contact_form = CommunityContactForm(request.POST)

        if community_partner_form.is_valid() and community_partner_contact_form.is_valid():
            community_partner_form.save()
            community_partner_contact_form.save()

            return render(request, 'home/community_partner_register_done.html', )
    else:
        community_partner_form = CommunityPartnerForm()
        community_partner_contact_form = CommunityContactForm()

    return render(request,
                  'home/community_partner_register.html',
                  {'community_partner_form': community_partner_form,
                   'community_partner_contact_form': community_partner_contact_form}, )


def uploadProject(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/uploadProject.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        form = ProjectForm(data_dict)
        if form.is_valid():
            form.save()
    return render(request, 'import/uploadProject.html',
                  {'uploadProject': uploadProject})


def uploadCommunity(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/uploadCommunity.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        form = CommunityForm(data_dict)
        if form.is_valid():
            form.save()
    return render(request, 'import/uploadCommunity.html',
                  {'uploadCommunity': uploadCommunity})



def uploadCampus(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/uploadCampus.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        form = CampusForm(data_dict)
        if form.is_valid():
            form.save()
    return render(request, 'import/uploadCampus.html',
                  {'uploadCampus': uploadCampus})

