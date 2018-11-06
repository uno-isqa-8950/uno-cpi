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


def CommunityHome(request):
    return render(request, 'home/Community_Home.html',
                  {'CommunityHome': CommunityHome})


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
    mission_dict = {}
    mission_list = []
    for m in missions:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.id for project in campus_filter.qs]
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]
        project_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
        print(project_ids)
        mission_dict['mission_name'] = m.mission_name
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).\
            filter(community_partner_id__in=community_list).count()
        mission_dict['project_count'] = project_count
        mission_dict['community_count'] = community_count
        total_uno_students = 0
        total_uno_hours = 0
        p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids)
        for pm in p_mission:
            uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        mission_dict['total_uno_hours'] = total_uno_hours
        mission_dict['total_uno_students'] = total_uno_students
        mission_list.append(mission_dict.copy())
    print(mission_list)
    return render(request, 'reports/14ProjectPartnerInfo.html',
                  {'project_filter': project_filter, 'mission_list': mission_list, 'campus_filter': campus_filter})


# (15) Engagement Summary Report: filter by Semester, MissionArea


def engagement_info(request):
    engagements = EngagementType.objects.all()
    eDict = {}
    eList = []
    for e in engagements:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.id for project in campus_filter.qs]
        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
        project_mission_ids = [p.id for p in missions_filter.qs]
        semester_filter = SemesterFilter(request.GET, queryset=Semester.objects.all())
        project_semester_ids = [p.id for p in semester_filter.qs]
        filtered_project_ids = list(set(project_mission_ids) | set(project_semester_ids))
        filtered_project_list = list(set(campus_filtered_ids).intersection(filtered_project_ids))
        eDict['engagement_name'] = e.name
        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list).count()
        eDict['project_count'] = project_count
        print(project_count)
        total_uno_students = 0
        total_uno_hours = 0
        projects = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)
        for p in projects:
            uno_students = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        eDict['total_uno_hours'] = total_uno_hours
        eDict['total_uno_students'] = total_uno_students
        eList.append(eDict.copy())
    return render(request, 'reports/15EngagementTypeReport.html',
                  {'missions_filter': missions_filter, 'semester_filter': semester_filter, 'eList': eList,
                   'campus_filter': campus_filter})


#Chart for projects with mission areas
def missionchart(request):

    missions = MissionArea.objects.all()
    mission_area1 = list()
    project_count_series_data = list()
    partner_count_series_data = list()

    for m in missions:
        filter2 = ProjectFilter(request.GET, queryset=Project.objects.all())
        proj_ids = [p.id for p in filter2.qs]
        mission_area1.append(m.mission_name)

        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id). \
            filter(community_partner_id__in=community_list).count()
        project_count_series_data.append(project_count)
        partner_count_series_data.append(community_count)

    print(mission_area1)
    print(partner_count_series_data)
    print(project_count_series_data)


    return render(request, 'charts/projectreport.html',
                  {
                      'mission': json.dumps(mission_area1),
                      'project_count_series': json.dumps(project_count_series_data),
                      'partner_count_series': json.dumps(partner_count_series_data),
                      'filter2': filter2
                  })



def EngagementType_Chart(request):
    project_engagement_count=[]
    engagment_community_counts=[]
    engagment_campus_counts=[]
    project_engagement_series=[]
    engagament_names=[]

    engagement_types = EngagementType.objects.all()
    for et in engagement_types:
        engagament_names.append(et.name)

        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
        project_mission_ids = [p.project_name_id for p in missions_filter.qs]

        semester_filter = SemesterFilter(request.GET, queryset=Semester.objects.all())
        project_semester_ids = [p.id for p in semester_filter.qs]
        proj_id_sem= Project.objects.filter(semester_id__in=project_semester_ids).filter(id__in = project_mission_ids)
        filtered_project_list = [p.id for p in proj_id_sem]

        project_count = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list).count()
        project_engagement_count.append(project_count)

        projects = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list)
        proj_ids = [p.id for p in projects]
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_community_counts.append(p_community)

        p_campus = ProjectCampusPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_campus_counts.append(p_campus)

    Max_count = max(list(set(project_engagement_count)|set(engagment_community_counts)|set(engagment_campus_counts)))

    project_engagement_series = {
        'name': 'Project Count',
        'data': project_engagement_count,
        'color': 'teal' }
    engagment_community_series = {
        'name': 'Community Partner Count',
        'data': engagment_community_counts,
        'color': 'turquoise' }
    engagment_campus_series = {
        'name': 'Campus Partner Count',
        'data': engagment_campus_counts,
        'color': 'blue' }

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': '   '},
        'xAxis': {'title':{'text': 'Engagement Types'},'categories': engagament_names},
        'yAxis' : {'title':{'text': 'Projects Engagement Count'},'min':0, 'max':Max_count+7},
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -40,
            'y': 80,
            'floating': 'true',
            'borderWidth': 1,
            'backgroundColor':  '#FFFFFF',
            'shadow': 'true'
        },
        'series': [project_engagement_series ,engagment_community_series ,engagment_campus_series]
    }

    dump = json.dumps(chart)
    return render(request, 'charts/engagementtypechart2.html',
                 {'chart': dump,'missions_filter':missions_filter,'semester_filter':semester_filter})