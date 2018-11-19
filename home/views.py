import json
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from home.decorators import campuspartner_required
from django.contrib.auth import authenticate, login, logout
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
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import EmailMessage



def home(request):
    return render(request, 'home/homepage.html',
                  {'home': home})

#def Contactus(request):
#    return render(request, 'home/ContactUs.html',
#                  {'Contactus': Contactus})

def Contactus(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
                , '')
            contact_email = request.POST.get(
                'contact_email'
                , '')
            topic =request.POST.get('topic','')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('home/contact_template.txt')
        context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'topic':topic,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "CPI Contact Form submission",
            content,
            "Community Partnership Initiative" + '',
            ['capstoneteam2018cpi@gmail.com'],
            headers={'Reply-To': contact_email}
        )
        email.send()
        return redirect('thanks')


    return render(request, 'home/contactus.html', {
    'form': form_class,
})

def thanks(request):
    return render(request, 'home/thanks.html',
                  {'thank': thanks})


def map(request):
    return render(request, 'home/Countymap.html',
                  {'map': map})

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

def AdminHome(request):
    user = authenticate(request)

    return render(request, 'home/admin_frame.html',
                  {'AdminHome': AdminHome})

def Adminframe(request):
    return render(request, 'home/admin_frame.html',
                  {'Adminframe': Adminframe})
def signup(request):
    return render(request, 'home/registration/signuporganization.html', {'signup': signup})


def signupuser(request):
    return render(request, 'home/registration/signupuser.html', {'signupuser': signupuser})


def registerCampusPartnerUser(request):
    campus_partner_user_form = CampusPartnerUserForm()
    user_form = CampususerForm()
    data = []
    for object in CampusPartner.objects.order_by('name'):
        data.append(object.name)
    if request.method == 'POST':
        user_form = CampususerForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)

        if user_form.is_valid() and campus_partner_user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_campuspartner = True
            new_user.save()

            campuspartneruser = CampusPartnerUser(campus_partner=campus_partner_user_form.cleaned_data['campus_partner'], user=new_user)
            campuspartneruser.save()

            return render(request, 'home/register_done.html', )
    else:
        user_form = CampususerForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)

    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form, 'data':data})


def registerCommunityPartnerUser(request):
    community_partner_user_form = CommunityPartnerUserForm()
    user_form = CommunityuserForm()
    commPartner = []
    for object in CommunityPartner.objects.order_by('name'):
        commPartner.append(object.name)

    if request.method == 'POST':
        user_form = CommunityuserForm(request.POST)
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
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form
                   ,'commPartner':commPartner})

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
            if form.is_valid():
                form.save()
                form_mission = UploadCommunityMissionForm(data_dict)
                print(form_mission)
                if form_mission.is_valid():
                    form_mission.save()
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
            print("data_dict", data_dict)
            college_count = College.objects.filter(college_name=data_dict['college_name']).count()
            print("college_count", college_count)
            if not college_count:
                form_college = UploadCollege(data_dict)
                if form_college.is_valid():
                    form_college.save()
                    form = UploadCampusForm(data_dict)
                    print(form)
                    if form.is_valid():
                        form.save()
            else:
                form = UploadCampusForm(data_dict)
                print ("form", form)
                if form.is_valid():
                    form.save()
    return render(request, 'import/uploadCampusDone.html')


# uploading the campus data via csv file

def upload_income(request):
    if request.method == 'GET':
        download_campus_url = '/media/household_income.csv'
        return render(request, 'import/uploadIncome.html',
                      {'download_campus_url': download_campus_url})
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data_dict = dict(OrderedDict(row))
            form = UploadIncome(data_dict)
            if form.is_valid():
                form.save()
    return render(request, 'import/uploadIncomeDone.html')


# (14) Mission Summary Report: filter by Semester, EngagementType


def project_partner_info(request):
    missions = MissionArea.objects.all()
    mission_dict = {}
    mission_list = []
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())

    for m in missions:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]
        project_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
        print(project_ids)
        mission_dict['mission_name'] = m.mission_name
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).distinct()
        print(p_community)
        community_list = [c.community_partner_id for c in p_community]
        print(community_list)
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).\
            filter(community_partner_id__in=community_list).count()
        print(community_count)
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
    # print(mission_list)
    return render(request, 'reports/14ProjectPartnerInfo.html',
                  {'project_filter': project_filter, 'mission_list': mission_list, 'campus_filter': campus_filter})


# (15) Engagement Summary Report: filter by AcademicYear, MissionArea


def engagement_info(request):
    engagements = EngagementType.objects.all()
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    eDict = {}
    eList = []
    for e in engagements:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
        project_mission_ids = [p.project_name_id for p in missions_filter.qs]
        year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_year_ids = [p.id for p in year_filter.qs]
        print(project_year_ids)
        filtered_project_ids = list(set(project_mission_ids).intersection(project_year_ids))
        filtered_project_list = list(set(campus_filtered_ids).intersection(filtered_project_ids))
        eDict['engagement_name'] = e.name
        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list).count()
        eDict['project_count'] = project_count
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
                  {'missions_filter': missions_filter, 'year_filter': year_filter, 'eList': eList,
                   'campus_filter': campus_filter})


# (15) Engagement Summary Report: filter by AcademicYear, MissionArea


def unique_count(request):
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    project_year_ids = [p.id for p in year_filter.qs]
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    mission_ids = [m.mission_id for m in missions_filter.qs]
    project_missions = [p.project_name_id for p in missions_filter.qs]
    print(project_missions)
    unique_project_ids = list(set(campus_filtered_ids).intersection(project_year_ids))
    total_unique_project = list(set(unique_project_ids).intersection(project_missions))
    unique_project = len(total_unique_project)

    #community partner count
    community_mission_filter = CommunityPartnerMission.objects.filter(mission_area_id__in=mission_ids)
    community_mission_ids = [c.community_partner_id for c in community_mission_filter]
    print(community_mission_filter)
    # unique_community_ids = ProjectCommunityPartner.objects.filter(project_name_id__in=unique_project_ids)
    # total_unique_community = list(set(community_mission_ids).intersection(unique_community_ids))
    unique_community = len(community_mission_ids)

    return render(request, 'reports/8CountOfUniqueCommunityPartner.html',
                  {'missions_filter': missions_filter, 'year_filter': year_filter,
                   'campus_filter': campus_filter, 'unique_project': unique_project,
                   'unique_community': unique_community, 'community_mission_filter': community_mission_filter})


# Chart for projects with mission areas

def missionchart(request):

    missions = MissionArea.objects.all()
    mission_area1 = list()
    project_count_series_data = list()
    partner_count_series_data = list()
    max_series_data = list()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    year_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())

    for m in missions:
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        proj_ids = [p.id for p in project_filter.qs]
        mission_area1.append(m.mission_name)
        year_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())
        proj_year_ids = [p.id for p in year_filter.qs]
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids).filter(project_name_id__in=proj_year_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).filter(project_name_id__in=proj_year_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id). \
            filter(community_partner_id__in=community_list).count()
        project_count_series_data.append(project_count)
        partner_count_series_data.append(community_count)


    Max_count = max(
            list(set(partner_count_series_data) | set(project_count_series_data)),default=1)
    max_series_data.append(Max_count)

    project_count_series = {
            'name': 'Project Count',
            'data': project_count_series_data,
            'color': 'turquoise'}
    partner_count_series = {
            'name': 'Community Partner Count',
            'data': partner_count_series_data,
            'color': 'teal'}

    chart = {
            'chart': {'type': 'bar'},
            'title': {'text': '   '},
            'xAxis': {'title': {'text': 'Mission Areas'}, 'categories': mission_area1},
            'yAxis': {'title': {'text': 'Projects Count'}, 'min': 0, 'max': Max_count + 5},
            'legend': {
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'top',
                'x': -40,
                'y': 80,
                'floating': 'true',
                'borderWidth': 1,
                'backgroundColor': '#FFFFFF',
                'shadow': 'true'
            },
            'series': [project_count_series, partner_count_series]
        }

    chart_dump = json.dumps(chart)
    return render(request, 'charts/missionchart.html',{'chart': chart_dump , 'project_filter' : project_filter , 'year_filter' :year_filter})


def EngagementType_Chart(request):
    project_engagement_count=[]
    engagment_community_counts=[]
    engagment_campus_counts=[]
    project_engagement_series=[]
    engagament_names=[]
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    academicyear_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())
    engagement_types = EngagementType.objects.all()
    for et in engagement_types:
        engagament_names.append(et.name)

        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
        project_mission_ids = [p.project_name_id for p in missions_filter.qs]

        #semester_filter = SemesterFilter(request.GET, queryset=Semester.objects.all())
        academicyear_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())
        project_academicyear_ids = [p.id for p in academicyear_filter.qs]
        proj_id_sem= Project.objects.filter(academic_year_id__in=project_academicyear_ids).filter(id__in = project_mission_ids)
        filtered_project_list = [p.id for p in proj_id_sem]

        project_count = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list).count()
        project_engagement_count.append(project_count)

        projects = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list)
        proj_ids = [p.id for p in projects]
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_community_counts.append(p_community)

        p_campus = ProjectCampusPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_campus_counts.append(p_campus)

    Max_count = max(list(set(project_engagement_count)|set(engagment_community_counts)|set(engagment_campus_counts)), default=1)

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
                 {'chart': dump,'missions_filter':missions_filter,'academicyear_filter':academicyear_filter})

######## export data to Javascript (Testing) ################################
def countyData(request):
    json_data = open('home/static/GEOJSON/NECounties2.geojson')
    countyData = json.load(json_data)
    return render(request, 'home/Countymap.html',
                  {'countyData': countyData})