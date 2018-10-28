import json
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from home.decorators import campuspartner_required
# CSV, OrderedDict are used for uploading the data
import csv
from collections import OrderedDict
# importing models in home views.py
from .models import *
from university.models import *
from partners.models import CampusPartnerUser, CommunityPartnerUser, CampusPartner, CommunityPartner, \
    CommunityPartnerMission
from projects.models import Project, EngagementType, ActivityType, Status, ProjectCampusPartner, ProjectMission, \
    ProjectCommunityPartner
# importing filters in home views.py, used for adding filter
from .filters import *
# aggregating function
from django.db.models import Sum
# importing forms into home views.py
from .forms import *


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})

def map(request):
    return render(request, 'home/testnew.html',
                  {'map': map})

def k12map(request):
    return render(request, 'home/k12.html',
                  {'k12map': k12map})

def projectmap(request):
    return render(request, 'home/projectmap.html',
                  {'projectmap': projectmap})

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
    user_form = UserForm1()
    print(campus_partner_user_form)
    data = []
    for object in CampusPartner.objects.order_by().distinct('name'):
        data.append(object.name)
    if request.method == 'POST':
        user_form = UserForm1(request.POST)
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
    user_form = UserForm1()
    if request.method == 'POST':
        user_form = UserForm1(request.POST)
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

# uploading the projects data via csv file


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

# uploading the community data via csv file


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

# uploading the campus data via csv file


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

# (14) Mission Summary Report: filter by Semester, EngagementType


def project_partner_info(request):
    missions = MissionArea.objects.all()
    mDict = {}
    mList = []
    for m in missions:
        f = ProjectFilter(request.GET, queryset=Project.objects.all())
        proj_ids = [p.id for p in f.qs]
        mDict['mission_name'] = m.mission_name
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).\
            filter(community_partner_id__in=community_list).count()
        mDict['project_count'] = project_count
        mDict['community_count'] = community_count
        total_uno_students = 0
        total_uno_hours = 0
        p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids)
        # pids = [pm.project_name_id for pm in p_mission]
        # uno_students1 = Project.objects.filter(id__in=p_mission).aggregate(Sum('total_uno_students'))
        # print(uno_students1)
        for pm in p_mission:
            uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        mDict['total_uno_hours'] = total_uno_hours
        mDict['total_uno_students'] = total_uno_students
        mList.append(mDict.copy())
    return render(request, 'reports/14ProjectPartnerInfo.html',
                  {'filter': f, 'mList': mList})

# (15) Engagement Summary Report: filter by Semester, EngagementType


def engagement_info(request):
    engagements = EngagementType.objects.all()
    eDict = {}
    eList = []
    for e in engagements:
        f = ProjectFilter(request.GET, queryset=Project.objects.all())
        proj_ids = [p.id for p in f.qs]
        eDict['engagement_name'] = e.name
        # project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids).count()
        # p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct()
        # community_list = [c.community_partner_id for c in p_community]
        # community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).\
        #     filter(community_partner_id__in=community_list).count()
        # mdict['project_count'] = project_count
        # mdict['community_count'] = community_count
        # total_uno_students = 0
        # total_uno_hours = 0
        # p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids)
        # pids = [pm.project_name_id for pm in p_mission]
        # uno_students1 = Project.objects.filter(id__in=p_mission).aggregate(Sum('total_uno_students'))
        # print(uno_students1)
        # for pm in p_mission:
        #     uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
        #     uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
        #     total_uno_students += uno_students['total_uno_students__sum']
        #     total_uno_hours += uno_hours['total_uno_hours__sum']
        # mdict['total_uno_hours'] = total_uno_hours
        # mdict['total_uno_students'] = total_uno_students
        eList.append(eDict.copy())
    return render(request, 'reports/15EngagementType.html',
                  {'filter': f, 'eList': eList})


#Report for projects with mission areas
def projectreport(request):
    mission_name = ProjectMission.objects \
        .values('mission') \
        .annotate(mission_type_count=Count('mission', filter=Q(mission_type='Primary')),
                  ) \
        .order_by('mission')
    print(mission_name)

    mission_area = list()
    project_count_series_data = list()

    print(mission_area)
    print(project_count_series_data)
    for entry in mission_name:
        mission_area.append('%s Mission' % entry['mission'])
        project_count_series_data.append(entry['mission_type_count'])

        project_count_series = {
        'name': 'Project Count',
        'data': project_count_series_data,
        'color': 'turquoise'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Projects in different Mission Areas'},
        'xAxis': {'mission': mission_area},
        'series': [project_count_series]
    }

    dump = json.dumps(chart)
    print(dump)
    print("hello")
    return render(request, 'reports/projectreport.html',
                  {'chart': dump})


