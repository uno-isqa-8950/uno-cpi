from django.db import connection
from django.forms import modelformset_factory
from home.decorators import campuspartner_required
from .models import *
from university.models import *
from partners.models import CampusPartnerUser, CommunityPartnerUser, CampusPartner, CommunityPartner, CommunityPartnerMission
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner
from .forms import UserForm, CampusPartnerUserForm, \
    CommunityPartnerUserForm, UploadProjectForm, UploadCommunityForm,  UploadCampusForm, \
    UploadProjectCommunityForm, UploadProjectCampusForm, UploadCollege, UploadDepartment, \
    UploadProjectMissionForm
from django.shortcuts import render
from django.urls import reverse
import csv
from collections import OrderedDict
from django.contrib import messages


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})

def about(request):
    return render(request, 'home/okMap.html',
                  {'map': map})

def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})


def campusHome(request):
    return render(request, 'home/Campus_Home.html',
                  {'campusHome': campusHome})

def signup(request):
    return render(request, 'home/registration/signuporganization.html', {'signup': signup})


def signupuser(request):
    return render(request, 'home/registration/signupuser.html', {'signupuser': signupuser})


def registerCampusPartnerUser(request):
    campus_partner_user_form = CampusPartnerUserForm()
    user_form = UserForm()
    print(campus_partner_user_form)
    data = []
    for object in CampusPartner.objects.order_by().distinct('name'):
        data.append(object.name)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)

        # community_partner_form = CommunityPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_user_form.is_valid():
            # and community_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_campuspartner = True
            new_user.save()

            # cpu = CampusPartnerUser(campuspartner=CampusPartner.objects.filter(
            #         campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0], user=new_user)
            campuspartneruser = CampusPartnerUser(campus_partner=campus_partner_user_form.cleaned_data['campus_partner'], user=new_user)
            campuspartneruser.save()

            return render(request, 'home/register_done.html', )
    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form, 'data':data})



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
            new_user.is_communitypartner = True
            new_user.save()
            # cpu = CommunityPartnerUser(communitypartner=CommunityPartner.objects.filter(
            #        name=community_partner_form.cleaned_data['name'])[0], user=new_user)
            communitypartneruser = CommunityPartnerUser(community_partner=community_partner_user_form.cleaned_data['community_partner'], user=new_user)
            communitypartneruser.save()
            return render(request, 'home/communityuser_register_done.html', )
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form})



def upload_project(request):
    if request.method == 'GET':
        download_projects_url = '/media/projects_sample.csv'
        return render(request, 'import/uploadProject.html',
                      {'download_projects_url': download_projects_url})
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data_dict = dict(OrderedDict(row))
            project_count = Project.objects.filter(project_name=data_dict['project_name']).count()
            if project_count == 1:
                form_campus = UploadProjectCampusForm(data_dict)
                form_community = UploadProjectCommunityForm(data_dict)
                form_mission = UploadProjectMissionForm(data_dict)
                print(form_mission)
                if form_campus.is_valid() and form_community.is_valid() and form_mission.is_valid():
                    form_campus.save()
                    form_community.save()
                    form_mission.save()
            elif project_count == 0:
                form = UploadProjectForm(data_dict)
                print(form)
                if form.is_valid():
                    form.save()
                    form_campus = UploadProjectCampusForm(data_dict)
                    form_community = UploadProjectCommunityForm(data_dict)
                    form_mission = UploadProjectMissionForm(data_dict)
                    if form_campus.is_valid and form_community.is_valid() and form_mission.is_valid():
                        form_campus.save()
                        form_community.save()
                        form_mission.save()
    return render(request, 'import/uploadProjectDone.html')


def upload_community(request):
    if request.method == 'GET':
        download_community_url = '/media/community_sample.csv'
        return render(request, 'import/uploadCommunity.html',
                      {'download_community_url': download_community_url})
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        community_count = CommunityPartner.objects.filter(name=data_dict['name']).count()
        if community_count == 0:
            form = UploadCommunityForm(data_dict)
            print(form)
            if form.is_valid():
                form.save()
    return render(request, 'import/uploadCommunityDone.html')


def upload_campus(request):
    if request.method == 'GET':
        download_campus_url = '/media/campus_sample.csv'
        return render(request, 'import/uploadCampus.html',
                      {'download_campus_url': download_campus_url})
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data_dict = dict(OrderedDict(row))
            college_count = College.objects.filter(college_name=data_dict['college_name']).count()
            if college_count == 0:
                form_college = UploadCollege(data_dict)
                if form_college.is_valid():
                    form_college.save()
                    form = UploadCampusForm(data_dict)
                    print(form)
                    if form.is_valid():
                        form.save()
            elif college_count == 1:
                form = UploadCampusForm(data_dict)
                if form.is_valid():
                    form.save()
    return render(request, 'import/uploadCampusDone.html')
