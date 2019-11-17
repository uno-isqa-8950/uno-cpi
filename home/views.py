import json
import logging
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from home.decorators import campuspartner_required, admin_required
from django.contrib.auth import authenticate, login, logout
import csv
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from collections import OrderedDict
import sys
sys.setrecursionlimit(1500)
# importing models in home views.py
from .models import *
from university.models import *
from partners.models import *
from projects.models import *
# importing filters in home views.py, used for adding filter
from .filters import *
# aggregating function
from django.db.models import Sum
from django.conf import settings
# importing forms into home views.py
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
import googlemaps
from shapely.geometry import shape, Point
import pandas as pd
import os
from googlemaps import Client
from home import context_processors
import boto3
from UnoCPI import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import sys
import psycopg2
import json
import datetime
# The imports below are for running sql queries for Charts
from django.db import connection
from UnoCPI import sqlfiles
from projects.forms import K12ChoiceForm,CecPartChoiceForm
from projects.models import AcademicYear

sql=sqlfiles
logger = logging.getLogger(__name__)
#writing into amazon s3 bucket
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

# Read JSON files for charts
charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')


#read Partner.geojson from s3
content_object_partner = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Partner.geojson')
partner_geojson = content_object_partner.get()['Body'].read().decode('utf-8')

#read Project.geojson from s3
content_object_project = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Project.geojson')
project_geojson = content_object_project.get()['Body'].read().decode('utf-8')

gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)

def countyGEO():
    with open('home/static/GEOJSON/USCounties_final.geojson') as f:
        geojson1 = json.load(f)

    county = geojson1["features"]
    return county


##### Get the district GEOJSON ##############
def districtGEO():
    with open('home/static/GEOJSON/ID2.geojson') as f:
        geojson = json.load(f)

    district = geojson["features"]
    return district


def home(request):
    return render(request, 'home/communityPartner.html',
                  {'home': home})


def MapHome(request):
    return render(request, 'home/Map_Home.html',
                  {'MapHome': MapHome})

def thanks(request):
    return render(request, 'home/thanks.html',
                  {'thank': thanks})


def partners(request):
    data_definition = DataDefinition.objects.all()
    return render(request, 'home/partners.html',
                  {'partners': partners,
                   'data_definition': data_definition})


def map(request):
    return render(request, 'home/Countymap.html',
                  {'map': map})


def districtmap(request):
    return render(request, 'home/Districtmap.html',
                  {'districtmap': districtmap})


def projectmap(request):
    return render(request, 'home/projectmap.html',
                  {'projectmap': projectmap})


def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})


@login_required()
def campusHome(request):
    return render(request, 'home/Campus_Home.html',
                  {'campusHome': campusHome})


@login_required()
def CommunityHome(request):
    return render(request, 'home/Community_Home.html',
                  {'CommunityHome': CommunityHome})


@login_required()
def AdminHome(request):
    user = authenticate(request)

    return render(request, 'home/admin_frame.html',
                  {'AdminHome': AdminHome})


@login_required()
def Adminframe(request):
    return render(request, 'home/admin_frame.html',
                  {'Adminframe': Adminframe})


def signup(request):
    return render(request, 'home/registration/signuporganization.html', {'signup': signup})


def signupuser(request):
    return render(request, 'home/registration/signupuser.html', {'signupuser': signupuser})

def recentchanges(request):
    #project app
    recent_project = Project.history.all().order_by('-history_date')[:100]
    recent_proj_mission = ProjectMission.history.all().order_by('-history_date')[:100]
    recent_proj_campus = ProjectCampusPartner.history.all().order_by('-history_date')[:100]
    recent_proj_comm = ProjectCommunityPartner.history.all().order_by('-history_date')[:100]
    #partner app
    recent_campus = CampusPartner.history.all().order_by('-history_date')[:100]
    recent_comm = CommunityPartner.history.all().order_by('-history_date')[:100]
    recent_comm_mission = CommunityPartnerMission.history.all().order_by('-history_date')[:100]
    #users and contacts
    # recent_user = User.history.all().order_by('-history_date')[:100]
    recent_contact = Contact.history.all().order_by('-history_date')[:50]

    return render(request, 'home/recent_changes.html', {'recent_project': recent_project, 'recent_proj_mission': recent_proj_mission,
                                                        'recent_proj_campus': recent_proj_campus, 'recent_proj_comm': recent_proj_comm,

                                                        'recent_campus': recent_campus, 'recent_comm':recent_comm, 'recent_comm_mission':recent_comm_mission,
                                                        'recent_contact':recent_contact})

def registerCampusPartnerUser(request):
    data = []
    for object in CampusPartner.objects.order_by('name'):
        data.append(object.name)
    if request.method == 'POST':
        user_form = CampususerForm(request.POST)
        campus_partner_user_form = CampusPartnerUserForm(request.POST)

        if user_form.is_valid() and campus_partner_user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.is_campuspartner = True
            new_user.save()

            campuspartneruser = CampusPartnerUser(
                campus_partner=campus_partner_user_form.cleaned_data['campus_partner'], user=new_user)
            campuspartneruser.save()
            # Send an email to the user with the token:
            mail_subject = 'UNO-CPI Campus Partner Registration'
            current_site = get_current_site(request)
            message = render_to_string('account/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = new_user.email
            email = EmailMessage(mail_subject, message,to=[to_email])
            email.send()
            return render(request, 'home/register_done.html')
    else:
        user_form = CampususerForm()
        campus_partner_user_form = CampusPartnerUserForm()
    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form, 'data': data})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/')
    else:
        return render(request, 'home/registration/register_fail.html')

@login_required()
def registerCommunityPartnerUser(request):
    community_partner_user_form = CommunityPartnerUserForm()
    user_form = CommunityuserForm()
    commPartner = []
    for object in CommunityPartner.objects.order_by('name'):
        commPartner.append(object.name)

    if request.method == 'POST':
        user_form = CommunityuserForm(request.POST)
        community_partner_user_form = CommunityPartnerUserForm(request.POST)
        if user_form.is_valid() and community_partner_user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_communitypartner = True
            new_user.save()
            communitypartneruser = CommunityPartnerUser(
                community_partner=community_partner_user_form.cleaned_data['community_partner'], user=new_user)
            communitypartneruser.save()
            return render(request, 'home/communityuser_register_done.html', )
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form
                      , 'commPartner': commPartner})


# uploading the projects data via csv file

@login_required()
@admin_required()
def upload_project(request):
    Missionlist=[]
    CampusPartnerlist=[]
    CommTypelist=[]
    if request.method == 'GET':
        download_projects_url = '/media/projects_sample.csv'
        return render(request, 'import/uploadProject.html',
                      {'download_projects_url': download_projects_url})
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('ISO 8859-1').splitlines()
        reader = csv.DictReader(decoded)
        campus_query = CampusPartner.objects.all()
        campus_names = [campus.name for campus in campus_query]
        community_query = CommunityPartner.objects.all()
        community_names = [community.name for community in community_query]
        for row in reader:
            data_dict = dict(OrderedDict(row))
            form = UploadProjectForm(data_dict)
            campus = data_dict['campus_partner'] in campus_names
            community = data_dict['community_partner'] in community_names
            if campus and community and form.is_valid():
                form.save()
                form_campus = UploadProjectCampusForm(data_dict)
                form_community = UploadProjectCommunityForm(data_dict)
                form_mission = UploadProjectMissionForm(data_dict)
                if form_campus.is_valid() and form_community.is_valid() and form_mission.is_valid():
                    form_campus.save()
                    form_community.save()
                    form_mission.save()

    return render(request, 'import/uploadProjectDone.html')


# uploading the community data via csv file


@login_required()
@admin_required()
def upload_community(request):
    if request.method == 'GET':
        download_community_url = '/media/community_sample.csv'
        return render(request, 'import/uploadCommunity.html',
                      {'download_community_url': download_community_url})
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('ISO 8859-1').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))

        form = UploadCommunityForm(data_dict)

        if form.is_valid():
            form.save()
            form_mission = UploadCommunityMissionForm(data_dict)
            if form_mission.is_valid():
                form_mission.save()
    return render(request, 'import/uploadCommunityDone.html')


# uploading the campus data via csv file


@login_required()
@admin_required()
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
            if not college_count:
                form_college = UploadCollege(data_dict)
                if form_college.is_valid():
                    form_college.save()
                    form = UploadCampusForm(data_dict)
                    if form.is_valid():
                        form.save()
            else:
                form = UploadCampusForm(data_dict)
                if form.is_valid():
                    form.save()
    return render(request, 'import/uploadCampusDone.html')


# uploading the campus data via csv file
@login_required()
@admin_required()
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


# (14) Mission Summary Report: filter by Semester, EngagementType - TRY 1
def project_partner_info(request):
    data_definition = DataDefinition.objects.all()
    focus_dict = {}
    focus_list = []
    subcat_dict = {}
    subcat_list = []
    subcat_proj_list = []
    subcat_comm_part_list = []
    focus_proj_list = []
    focus_comm_part_list = []
    focus_proj_total = 0
    focus_comm_total = 0
    focus_students_total = 0
    focus_hours_total = 0
    prev_focus_area = None
    curr_focus_area = None

    data_list=[]
    legislative_choices = []
    legislative_search = ''
    data_definition = DataDefinition.objects.all()
    status_draft = Status.objects.filter(name='Drafts')

    #set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1,50):
        legistalive_val = 'Legislative District '+str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]


    #set legislative_selection on template choices field -- Manu End

    #set k12 flag on template choices field
    k12_selection = request.GET.get('k12_flag', None)
    k12_init_selection = "All"
    if k12_selection is None:
        k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    #set cec partner flag on template choices field
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_init_selection = "All"
    if cec_part_selection is None:
        cec_part_selection = cec_part_init_selection
    #print('CEC Partner set in view ' + cec_part_selection)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    # if k12_selection == 'Yes':
    #     if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
    #         project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True))
    #     else:
    #         project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True).filter(legislative_district=legislative_search))
    # elif k12_selection == 'No':
    #      if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
    #         project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False))
    #      else:
    #         project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False).filter(legislative_district=legislative_search))
    # else:
    #     if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    #     else:
    #         project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(legislative_district=legislative_search))
    #
    #
    # if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    # else:
    #     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(legislative_district=legislative_search))
    # legislative district end -- Manu

    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all()) # commented by Manu
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all()) # commented by Manu

    community_filtered_ids = communityPartners.qs.values_list('id',flat=True)
    # community_filtered_ids = [community.id for community in communityPartners.qs]
    community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(community_partner_id__in=community_filtered_ids))
    # community_project_filtered_ids = [project.project_name_id for project in community_project_filter.qs]
    community_project_filtered_ids = community_project_filter.qs.values_list('project_name', flat=True)

    campus_filtered_ids = campusPartners.qs.values_list('id',flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_filtered_ids))
    # campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    mission_filtered_ids = missions.qs.values_list('project_name', flat=True)
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)

    # Finding intersection of all the filters
    proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    proj_ids2 = list(set(proj_ids1).intersection(project_filtered_ids))
    project_ids = list(set(proj_ids2).intersection(community_project_filtered_ids))

    # To get the projects which does not have community partners
    projects_comm_ids = list(set(proj_ids2).difference(set(project_ids)))
    # projects_comm = list(Project.objects.filter(id__in=projects_comm_ids))

    #List of all Projects with Campus, Community Partners and have Mission
    # projects = list(Project.objects.filter(id__in=project_ids))
    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond =  mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond =  community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond =  campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond =  college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=campus_partner_filter)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        legislative_district_cond = '%'

    else:
        legislative_district_cond = legislative_search

    academic_year_filter = request.GET.get('academic_year', None)
    acad_years = AcademicYear.objects.all()
    yrs = []
    for e in acad_years:
        yrs.append(e.id)
    max_yr_id = max(yrs)
    print("max_yr_id", max_yr_id)
    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = int(max_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond =  'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    params = [eng_type_cond,
              academic_start_year_cond,
              academic_end_year_cond,
              mission_type_cond,
              college_unit_cond,
              campus_partner_cond,
              #cec_part_cond,
              community_type_cond,
              K12_filter_cond,
              legislative_district_cond,
              eng_type_cond,
              academic_start_year_cond,
              academic_end_year_cond,
              mission_type_cond,
              college_unit_cond,
              campus_partner_cond,
              # cec_part_cond,
              community_type_cond,
              K12_filter_cond,
              legislative_district_cond]

    print('Params:' , params)

    cursor = connection.cursor()
    cursor.execute(sql.missionSubcat_sql, params)
    for obj in cursor.fetchall():
        rec_type = obj[0]
        if rec_type == 'SUMMARY':
            focus_dict['id'] = obj[1]
            focus_dict['mission_name'] = obj[2]
            focus_dict['subcategory'] = obj[3]
            focus_dict['project_count'] = obj[4]
            focus_dict['community_count'] = obj[5]
            focus_dict['total_uno_students'] = obj[6]
            focus_dict['total_uno_hours'] = obj[7]
            focus_dict['mission_desc'] = obj[8]

            if focus_dict['community_count'] != '' and focus_dict['community_count'] is not None and focus_dict['community_count'] > 0:
                focus_comm_total += focus_dict['community_count']
            if focus_dict['project_count'] != '' and focus_dict['project_count'] is not None and focus_dict['project_count'] > 0:
                focus_proj_total += focus_dict['project_count']
            if focus_dict['total_uno_students'] != '' and focus_dict['total_uno_students'] is not None and focus_dict['total_uno_students'] > 0:
                focus_students_total += focus_dict['total_uno_students']
            if focus_dict['total_uno_hours'] != '' and focus_dict['total_uno_hours'] is not None and focus_dict['total_uno_hours'] > 0:
                focus_hours_total += focus_dict['total_uno_hours']

            focus_list.append(focus_dict.copy())

        elif rec_type == 'DETAILS':
            curr_focus_area = obj[1]  # set curr_focus_area

            # first detail record - set previous focus area for compare
            if prev_focus_area is None:
                prev_focus_area = curr_focus_area

            #Set current subcat record values
            subcat_dict['id'] = obj[1]
            subcat_dict['mission_name'] = obj[2]
            subcat_dict['subcategory'] = obj[3]

            subcat_dict['project_count'] = obj[4]
            subcat_dict['community_count'] = obj[5]
            subcat_dict['total_uno_students'] = obj[6]
            subcat_dict['total_uno_hours'] = obj[7]
            subcat_list.append(subcat_dict.copy())
        else:
            print('Invalid record type')

    print('Focus Data')
    print(str(focus_list))
    print('totals data: ' +
          'focus_comm_total: ' + str(focus_comm_total) + ' ' +
          'focus_proj_total: ' + str(focus_proj_total) + ' ' +
          'focus_students_total: ' + str(focus_students_total) + ' ' +
          'focus_hours_total: ' + str(focus_hours_total))
    print('Subcat Data')
    print(str(subcat_list))

    '''
    cursor = connection.cursor()
    cursor.execute(sql.missionSubcat_Details_sql, params)
    for obj in cursor.fetchall():
        rec_type = obj[0]
        if rec_type == 'SUMMARY':
    '''


    return render(request, 'reports/ProjectPartnerInfo.html',
                  {'data_definition': data_definition,
                   'focus_list': focus_list, 'subcat_list': subcat_list,
                   'legislative_choices': legislative_choices, 'legislative_value':legislative_selection,
                   'focus_proj_total': focus_proj_total, 'focus_comm_total': focus_comm_total,
                   'focus_students_total': focus_students_total,'focus_hours_total': focus_hours_total,
                   'campus_id': campus_id, 'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,
                   "missions": missions, "communityPartners": communityPartners,
                   "campus_filter": campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id})

'''

def project_partner_info(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    mission_dict = {}
    mission_list = []
    proj_total = 0
    comm_total = 0
    students_total = 0
    hours_total = 0

    legislative_choices = []
    legislative_search = ''
   
    #set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    status_draft = Status.objects.filter(name='Drafts')
    #status_draft_ids = status_draft.qs.value_list('id', flat=True)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1,50):
        legistalive_val = 'Legislative District '+str(i)
        legislative_choices.append(legistalive_val)
    
    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(legislative_district=legislative_search))
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(legislative_district=legislative_search).exclude(status__in=status_draft))
    # legislative district end -- Manu


    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all()) -- commented by Manu
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all()) -- commented by Manu
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())


    # college_filtered_ids = [campus.id for campus in college_filter.qs]
    college_filtered_ids = college_filter.qs.values_list('id',flat=True)
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=college_filtered_ids))
    # campus_project_filter_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_project_filter_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    # campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
    campus_filtered_ids = campus_filter.qs.values_list('project_name', flat=True)

    # project_filtered_ids = [project.id for project in project_filter.qs]
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)
    print ('project_filtered_ids :', project_filtered_ids)
    #project_filtered_ids = list(set(project_filtered_ids1).difference(project_drafted_ids))

    # community_filtered_ids = [community.id for community in communityPartners.qs]
    community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
    comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(community_partner_id__in=community_filtered_ids))
    # comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]
    comm_filtered_ids = comm_filter.qs.values_list('project_name', flat=True)

    proj1_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
    proj2_ids = list(set(campus_project_filter_ids).intersection(proj1_ids))
    project_ids = list(set(proj2_ids).intersection(comm_filtered_ids))

    proj_comm = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).filter(community_partner_id__in=community_filtered_ids).distinct()
    proj_comm_ids = [community.community_partner_id for community in proj_comm]

    for m in missions:
        project_id_list=[]
        mission_dict['id'] = m.id
        mission_dict['mission_name'] = m.mission_name
        mission_dict['description'] = m.description
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_filtered_ids).filter(mission_type='Primary').count()
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=proj_comm_ids).count()
        comm_id_filter = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=proj_comm_ids)
        comm_id_list = list(community.community_partner_id for community in comm_id_filter)
        p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_filtered_ids).filter(mission_type='Primary')

        a = request.GET.get('engagement_type', None)
        b = request.GET.get('academic_year', None)
        c = request.GET.get('campus_partner', None)
        d = request.GET.get('college_name', None)
        if a is None or a == "All" or a == '':
            if b is None or b == "All" or b == '':
                if c is None or c == "All" or c == '':
                    if d is None or d == "All" or d == '':
                        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=community_filtered_ids).count()
                        comm_id_filter = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=community_filtered_ids)
                        comm_id_list = list(community.community_partner_id for community in comm_id_filter)

        e = request.GET.get('community_type', None)
        f = request.GET.get('weitz_cec_part', None)
        if f is None or f == "All" or f == '':
            if e is None or e == "All" or e == '':
                p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_filtered_ids).filter(mission_type='Primary')
                project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_filtered_ids).filter(mission_type='Primary').count()

        mission_dict['project_count'] = project_count
        mission_dict['community_count'] = community_count
        total_uno_students = 0
        total_uno_hours = 0

        for pm in p_mission:
            project_id_list.append(pm.project_name_id)
            uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']

        mission_dict['total_uno_hours'] = total_uno_hours
        mission_dict['total_uno_students'] = total_uno_students
        mission_dict['project_id_list'] = project_id_list
        mission_dict['comm_id_list'] = comm_id_list
        comm_ids = ''
        name_count=0

        for i in comm_id_list:
            comm_ids = comm_ids+str(i)

            if name_count < len(comm_id_list)-1:
                comm_ids = comm_ids + str(",")
                name_count = name_count + 1

        mission_dict['comm_ids'] = comm_ids

        project_name_id = ''
        project_name_count =0

        for z in project_id_list:
            project_name_id = project_name_id + str(z)

            if project_name_count < len(project_id_list)-1:
                project_name_id = project_name_id + str(",")
                project_name_count = project_name_count + 1

        mission_dict['project_name_ids'] =project_name_id

        mission_list.append(mission_dict.copy())
        proj_total += project_count
        comm_total += community_count
        students_total += total_uno_students
        hours_total += total_uno_hours

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id = college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)
    return render(request, 'reports/ProjectPartnerInfo.html',
                  {'project_filter': project_filter, 'data_definition': data_definition,
                  'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                   'communityPartners': communityPartners, 'mission_list': mission_list,
                   'campus_filter': campus_filter, 'college_filter': college_filter,
                   'proj_total': proj_total, 'comm_total': comm_total, 'students_total': students_total,
                   'hours_total': hours_total, 'campus_id':campus_id})
'''


# (15) Engagement Summary Report: filter by AcademicYear, MissionArea


def engagement_info(request):
    logger.info('Start engagement_info')
    engagements = EngagementType.objects.all()
    data_definition = DataDefinition.objects.all()
    engagement_Dict = {}
    engagement_List = []
    status_draft = Status.objects.filter(name='Drafts')
    #set legislative_selection on template choices field -- by Manu
    legislative_choices = []
    legislative_search = '';
    
    legislative_selection = request.GET.get('legislative_value', None)
   
    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1,50):
        legistalive_val = 'Legislative District '+str(i)
        legislative_choices.append(legistalive_val)
    
    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    # legislative selectionn end by Manu
             
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_campus_filtered_ids = [campus.campus_partner_id for campus in campus_project_filter.qs]

    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    project_mission_ids = [p.project_name_id for p in missions_filter.qs]

    
    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        year_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    else:
        year_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(legislative_district=legislative_search).exclude(status__in=status_draft))
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(legislative_district=legislative_search))
    
    project_year_ids = [project.id for project in year_filter.qs]

    community_filtered_ids = [community.id for community in communityPartners.qs]
    comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(community_partner_id__in=community_filtered_ids))
    comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]

    filtered_project_ids = list(set(project_mission_ids).intersection(project_year_ids))
    filtered_project_ids2 = list(set(campus_project_filtered_ids).intersection(filtered_project_ids))
    filtered_project_ids1 = list(set(campus_filtered_ids).intersection(filtered_project_ids2))
    filtered_project_list = list(set(comm_filtered_ids).intersection(filtered_project_ids1))
    for e in engagements:
        # gets the prpject ids for one engagement type
        proj_comm = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)
        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_comm_1 = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_comm).filter(community_partner_id__in=community_filtered_ids).distinct()
        # gets all the community partner ids in a array. These are not distinct
        proj_comm_ids = [community.community_partner_id for community in proj_comm_1]
        # sets the non distinct array to a distinct set of community partner ids
        unique_comm_ids = set(proj_comm_ids)
        comm_id_list = list(unique_comm_ids)
        # counts within the set of unique community partner ids
        unique_comm_ids_count = len(unique_comm_ids)

        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=project_year_ids).count()
        projects = Project.objects.filter(engagement_type_id=e.id).filter(id__in=project_year_ids)
        proj_ids_list = []
        proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_comm).filter(campus_partner_id__in=campus_campus_filtered_ids).distinct()
        proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]
        unique_camp_ids = set(proj_camp_ids)

        unique_camp_ids_count = len(unique_camp_ids)

        a = request.GET.get('weitz_cec_part', None)
        b = request.GET.get('community_type', None)
        if a is None or a == "All" or a == '':
            if b is None or b == "All" or b == '':
                project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1).count()
                projects = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1)
                proj_camp1 = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1)
                proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_camp1).filter(campus_partner_id__in=campus_campus_filtered_ids).distinct()
                proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]
                #comm_id_list = list(campus.campus_partner_id for campus in proj_camp)
                unique_camp_ids = set(proj_camp_ids)

                unique_camp_ids_count = len(unique_camp_ids)

        engagement_Dict['engagement_name'] = e.name
        engagement_Dict['description'] = e.description
        engagement_Dict['project_count'] = project_count
        engagement_Dict['community_count'] = unique_comm_ids_count
        engagement_Dict['campus_count'] = unique_camp_ids_count
        comm_ids = ''
        name_count = 0

        for i in comm_id_list:
            comm_ids = comm_ids + str(i)

            if name_count < len(comm_id_list) - 1:
                comm_ids = comm_ids + str(",")
            name_count = name_count + 1
        engagement_Dict['comm_id_list'] = comm_ids
        total_uno_students = 0
        total_uno_hours = 0

        for p in projects:
            proj_ids_list.append(p.id)
            uno_students = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        proj_ids = ''
        project_count = 0
        for i in proj_ids_list:
            proj_ids = proj_ids + str(i)

            if project_count < len(proj_ids_list) - 1:
                proj_ids = proj_ids + str(",")
                project_count = project_count + 1
        engagement_Dict['total_uno_hours'] = total_uno_hours
        engagement_Dict['total_uno_students'] = total_uno_students
        engagement_Dict['project_id_list'] = proj_ids
        engagement_List.append(engagement_Dict.copy())
        # proj_total += project_count
        # comm_total += unique_comm_ids_count
        # camp_total += unique_camp_ids_count
        # students_total += total_uno_students
        # hours_total += total_uno_hours

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id = college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)
    logger.info('End engagement_info')
    return render(request, 'reports/EngagementTypeReport.html',
                  {'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                      'college_filter': campus_partner_filter, 'missions_filter': missions_filter, 'year_filter': year_filter, 'engagement_List': engagement_List,
                   'data_definition':data_definition, 'communityPartners' : communityPartners ,'campus_filter': campus_filter, 'campus_id':campus_id})



# Chart for projects with mission areas

def missionchart(request):
    missions = MissionArea.objects.all()
    mission_area1 = list()
    data_definition = DataDefinition.objects.all()
    project_count_data = list()
    partner_count_data = list()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    for m in missions:
        college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        college_filtered_ids = [campus.id for campus in college_filter.qs]
        campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
            campus_partner_id__in=college_filtered_ids))
        campus_project_filter_ids = [project.project_name_id for project in campus_project_filter.qs]

        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]

        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        community_filtered_ids = [community.id for community in communityPartners.qs]

        comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
            community_partner_id__in=community_filtered_ids))
        comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]

        proj1_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
        proj2_ids = list(set(campus_project_filter_ids).intersection(proj1_ids))
        project_ids = list(set(proj2_ids).intersection(comm_filtered_ids))

        mission_area1.append(m.mission_name)
        project_count = ProjectMission.objects.filter(mission=m.id).filter(mission_type='Primary').filter(project_name_id__in=project_ids).count()

        proj_comm = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).filter(
            community_partner_id__in=community_filtered_ids).distinct()
        proj_comm_ids = [community.community_partner_id for community in proj_comm]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(
            community_partner_id__in=proj_comm_ids).count()

        a = request.GET.get('engagement_type', None)
        b = request.GET.get('academic_year', None)
        c = request.GET.get('campus_partner', None)
        d = request.GET.get('college_name', None)
        if a is None or a == "All" or a == '':
            if b is None or b == "All" or b == '':
                if c is None or c == "All" or c == '':
                    if d is None or d == "All" or d == '':
                        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(
                            community_partner_id__in=community_filtered_ids).count()

        e = request.GET.get('community_type', None)
        f = request.GET.get('weitz_cec_part', None)
        if f is None or f == "All" or f == '':
            if e is None or e == "All" or e == '':
                project_count = ProjectMission.objects.filter(mission=m.id).filter(mission_type='Primary').filter(
                    project_name_id__in=proj2_ids).count()

        project_count_data.append(project_count)
        partner_count_data.append(community_count)
    Max_count = max(list(set(partner_count_data) | set(project_count_data)), default=1)


    project_count_series = {
        'name': 'Project Count',
        'data': project_count_data,
        'color': 'turquoise'}
    partner_count_series = {
        'name': 'Community Partner Count',
        'data': partner_count_data,
        'color': 'teal'}
    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': '   '},
        'xAxis': {
            'title': {'text': 'Mission Areas', 'style': {'fontWeight': 'bold', 'color': 'black', 'fontSize': '15px'}},
            'categories': mission_area1, 'labels': {'style': {'color': 'black', 'fontSize': '13px'}}},
        'yAxis': {'allowDecimals': False, 'title': {'text': 'Projects/Community Partners ',
                                                    'style': {'fontWeight': 'bold', 'color': 'black',
                                                              'fontSize': '15px'}}, 'min': 0, 'max': Max_count + 5},
        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': 'true',
                    'style': {
                        'fontSize': '9px'
                    }
                }
            }
        },
        'legend': {
            'layout': 'horizontal',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -10,
            'y': 50,
            'borderWidth': 1,
            'backgroundColor': '#FFFFFF',
            'shadow': 'true'
        },
        'series': [project_count_series, partner_count_series]
    }

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)

    dump = json.dumps(chart)
    return render(request, 'charts/missionchart.html',
                  {'chart': dump, 'project_filter': project_filter, 'data_definition': data_definition,
                    'campus_filter': campus_filter, 'communityPartners': communityPartners, 'college_filter':college_filter, 'campus_id':campus_id})

def partnershipintensity(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    legislative_choices = []
    legislative_search = ''
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(legislative_district=legislative_search))
        project_filter = ProjectFilter(request.GET,queryset=Project.objects.filter(legislative_district=legislative_search))

    k12_selection = request.GET.get('k12_flag', None)
    k12_init_selection = "All"
    if k12_selection is None:
        k12_selection = k12_init_selection
    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    y_selection = request.GET.get('y_axis', None)
    y_init_selection = "years"
    if y_selection is None:
        y_selection = y_init_selection
    y_choices = YChoiceForm(initial={'y_choice': y_selection})

    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id = college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    missionList = []
    for m in MissionArea.objects.all():
        res = {'id': m.id, 'name': m.mission_name}
        missionList.append(res)
    missionList = sorted(missionList, key=lambda i: i['name'])

    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)

    return render(request, 'charts/partnershipintensity.html',
                  {'data_definition': data_definition, 'project_filter': project_filter,
                  'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                   'communityPartners': communityPartners, 'campus_filter': campus_filter,
                   'college_filter': college_filter, 'k12_choices': k12_choices, 'y_choices': y_choices,
                   'CommunityPartners': CommunityPartners, 'missionList': missionList,
                   'Projects':Projects, 'CampusPartners':CampusPartners})


# Trend Report Chart
@login_required()
@admin_required()
def trendreport(request):
    data_definition = DataDefinition.objects.all()

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    #set cec partner flag on template choices field
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_init_selection = "All"
    if cec_part_selection is None:
        cec_part_selection = cec_part_init_selection
    # print('CEC Partner set in view ' + cec_part_selection)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    yearList = []
    for y in AcademicYear.objects.all():
        res = {'id': y.id, 'name': y.academic_year}
        yearList.append(res)

    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)

    return render(request, 'charts/trendreport.html',
                  { 'missions_filter': missions_filter, 'project_filter': project_filter, 'data_definition': data_definition,
                    'campus_filter': campus_filter, 'college_filter':college_filter, 'communityPartners': communityPartners,
                    'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,'campus_filter': campus_filter, 'k12_choices': k12_choices,
                    'CommunityPartners': CommunityPartners, 'Projects':Projects, 'CampusPartners':CampusPartners, 'yearList':yearList})


def EngagementType_Chart(request):
    engagements = EngagementType.objects.all()
    data_definition = DataDefinition.objects.all()
    project_engagement_count = []
    engagment_community_counts = []
    engagment_campus_counts = []
    project_engagement_series = []
    engagament_names = []

    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_campus_filtered_ids = [campus.campus_partner_id for campus in campus_project_filter.qs]

    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    project_mission_ids = [p.project_name_id for p in missions_filter.qs]

    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    project_year_ids = [project.id for project in year_filter.qs]

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    community_filtered_ids = [community.id for community in communityPartners.qs]
    comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(community_partner_id__in=community_filtered_ids))
    comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]

    filtered_project_ids = list(set(project_mission_ids).intersection(project_year_ids))
    filtered_project_ids2 = list(set(campus_project_filtered_ids).intersection(filtered_project_ids))
    filtered_project_ids1 = list(set(campus_filtered_ids).intersection(filtered_project_ids2))
    filtered_project_list = list(set(comm_filtered_ids).intersection(filtered_project_ids1))


    for e in engagements:
        # gets the prpject ids for one engagement type
        proj_comm = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)
        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_comm_1 = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_comm).filter(community_partner_id__in=community_filtered_ids).distinct()
        # gets all the community partner ids in a array. These are not distinct
        proj_comm_ids = [community.community_partner_id for community in proj_comm_1]
        # sets the non distinct array to a distinct set of community partner ids
        unique_comm_ids = set(proj_comm_ids)
        # counts within the set of unique community partner ids
        unique_comm_ids_count = len(unique_comm_ids)

        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list).count()
        proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_comm).filter(campus_partner_id__in=campus_campus_filtered_ids).distinct()
        proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]
        unique_camp_ids = set(proj_camp_ids)
        unique_camp_ids_count = len(unique_camp_ids)

        a = request.GET.get('weitz_cec_part', None)
        b = request.GET.get('community_type', None)
        if a is None or a == "All" or a == '':
            if b is None or b == "All" or b == '':
                project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1).count()
                proj_camp1 = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1)
                proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_camp1).filter(campus_partner_id__in=campus_campus_filtered_ids).distinct()
                proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]
                unique_camp_ids = set(proj_camp_ids)
                unique_camp_ids_count = len(unique_camp_ids)

        project_engagement_count.append(project_count)
        engagment_community_counts.append(unique_comm_ids_count)
        engagment_campus_counts.append(unique_camp_ids_count)
        engagament_names.append(e.name)

    Max_count = max(list(set(project_engagement_count) | set(engagment_community_counts) | set(engagment_campus_counts))
                    , default=1)

    project_engagement_series = {
        'name': 'Project Count',
        'data': project_engagement_count,
        'color': 'teal'}
    engagment_community_series = {
        'name': 'Community Partner Count',
        'data': engagment_community_counts,
        'color': 'turquoise' }
    engagment_campus_series = {
        'name': 'Campus Partner Count',
        'data': engagment_campus_counts,
        'color': 'blue'}

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': '   '},
        'xAxis': {'title': {'text': 'Engagement Types','style':{'fontWeight': 'bold','color': 'black','fontSize': '15px'}},'categories': engagament_names,'labels': {'style':{'color': 'black','fontSize': '13px'} }},
        'yAxis': {'allowDecimals': False,'title': {'text': 'Projects/Partners','style':{'fontWeight': 'bold','color': 'black','fontSize': '15px'} }, 'min': 0, 'max': Max_count+15},

        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': 'true',
                    'style': {
                        'fontSize': '8px'
                    }
                }
            }
        },

        'legend': {
            'layout': 'horizontal',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -40,
            'y': -5,
            'borderWidth': 1,
            'backgroundColor':  '#FFFFFF',
            'shadow': 'true'
        },
        'series': [project_engagement_series, engagment_community_series, engagment_campus_series]
    }

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)

    dump = json.dumps(chart)
    return render(request, 'charts/engagementtypechart2.html',
                 {'chart': dump, 'missions_filter': missions_filter, 'academicyear_filter': year_filter,'data_definition':data_definition,
                  'campus_filter': campus_filter, 'communityPartners' : communityPartners, 'college_filter': campus_partner_filter, 'campus_id':campus_id})


def GEOJSON():
    # if (os.path.isfile('home/static/GEOJSON/Partner.geojson')):  # check if the GEOJSON is already in the DB
    #     with open('home/static/GEOJSON/Partner.geojson') as f:
    #         geojson1 = json.load(f)  # get the GEOJSON
    #     collection = geojson1  # assign it the collection variable to avoid changing the other code
    collection = json.loads(partner_geojson)
    mission_list = MissionArea.objects.all()
    mission_list = [m.mission_name for m in mission_list]
    CommTypelist = CommunityType.objects.all()
    CommTypelist = [m.community_type for m in CommTypelist]
    CampusPartner_qs = CampusPartner.objects.all()
    CampusPartnerlist = [{'name':m.name, 'c_id':m.college_name_id} for m in CampusPartner_qs]
    collegeName_list = College.objects.all()
    collegeName_list = collegeName_list.exclude(college_name__exact="N/A")
    collegeNamelist = [{'cname': m.college_name, 'id': m.id} for m in collegeName_list]
    yearlist=[]
    for year in AcademicYear.objects.all():
        yearlist.append(year.academic_year)
    commPartnerlist = CommunityPartner.objects.all()
    commPartnerlist = [m.name for m in commPartnerlist]
    return (collection, sorted(mission_list), sorted(CommTypelist), (CampusPartnerlist), sorted(yearlist),
            sorted(commPartnerlist), (collegeNamelist))


######## export data to Javascript for Household map ################################
def countyData(request):
    Campuspartner = GEOJSON()[3]
    data = GEOJSON()[0]
    # Campuspartner = set(Campuspartner[0])
    # Campuspartner = list(Campuspartner)
    json_data = open('home/static/GEOJSON/USCounties_final.geojson')
    county = json.load(json_data)

    return render(request, 'home/Countymap.html',
                  {'countyData': county, 'collection': GEOJSON()[0],
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4]
                   }
                  )



def GEOJSON2():
    # if (os.path.isfile('home/static/GEOJSON/Project.geojson')):  # check if the GEOJSON is already in the DB
    #     with open('home/static/GEOJSON/Project.geojson') as f:
    #         geojson1 = json.load(f)  # get the GEOJSON
    #     collection = geojson1  # assign it the collection variable to avoid changing the other code
    collection = json.loads(project_geojson)
    Missionlist = []  ## a placeholder array of unique mission areas
    Engagementlist = []
    Academicyearlist = []
    CommunityPartnerlist = []
    CampusPartnerlist = []
    CommunityPartnerTypelist = []
    CollegeNamelist = []

    for e in CommunityType.objects.all():
        if (str(e.community_type) not in CommunityPartnerTypelist):
            CommunityPartnerTypelist.append(str(e.community_type))

    for e in College.objects.all():
        if(str(e.college_name) not in CollegeNamelist):
            if (str(e.college_name) != "N/A"):
                CollegeNamelist.append({'cname':str(e.college_name), 'id':e.id})


    for year in AcademicYear.objects.all():
        Academicyearlist.append(year.academic_year)

    for mission in MissionArea.objects.all():
        Missionlist.append(mission.mission_name)

    for engagement in EngagementType.objects.all():
        Engagementlist.append(engagement.name)

    for communitypart in CommunityPartner.objects.all():
        CommunityPartnerlist.append(communitypart.name)

    for campuspart in CampusPartner.objects.all():
        CampusPartnerlist.append({'name': campuspart.name, 'c_id': campuspart.college_name_id})


    return (collection, sorted(Engagementlist),sorted(Missionlist),sorted(CommunityPartnerlist),
            (CampusPartnerlist), sorted(CommunityPartnerTypelist),sorted(Academicyearlist), (CollegeNamelist))


###Project map export to javascript
def googleprojectdata(request):
    data_definition = DataDefinition.objects.all()
    Campuspartner = GEOJSON2()[4]
    Communitypartner = GEOJSON2()[3]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    data = GEOJSON2()[0]
    return render(request, 'home/projectMap.html',
                  {'districtData': district, 'collection': GEOJSON2()[0],
                   'number': len(data['features']),
                   'Missionlist': sorted(GEOJSON2()[2]),
                   'CommTypelist': sorted(GEOJSON2()[5]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'Communitypartner': sorted(Communitypartner),
                   'EngagementType': sorted(GEOJSON2()[1]),
                   'year': sorted(GEOJSON2()[6]),'data_definition':data_definition,
                   'Collegename': (GEOJSON2()[7])
                   }
                  )


def googleDistrictdata(request):
    data_definition = DataDefinition.objects.all()
    Campuspartner = GEOJSON()[3]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/legislativeDistrict.html',
                  {'districtData': district, 'collection': GEOJSON()[0],
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'number': len(data['features']),
                   'year': sorted(GEOJSON()[4]),'data_definition':data_definition,
                   'Collegename': GEOJSON()[6]
                   }
                  )


def googlepartnerdata(request):
    data_definition = DataDefinition.objects.all()
    map_json_data = GEOJSON()
    Campuspartner = map_json_data[3]
    College = map_json_data[6]
    data = map_json_data[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/communityPartner.html',
                  {'collection': data, 'districtData':district,
                   'Missionlist': sorted(map_json_data[1]),
                   'CommTypeList': sorted(map_json_data[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'number': len(data['features']),
                   'year': map_json_data[4],'data_definition':data_definition,
                   'College': (College) #k sorted
                   }
                  )


def googlemapdata(request):
    data_definition = DataDefinition.objects.all()
    Campuspartner = GEOJSON()[3]
    College = GEOJSON()[6]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/communityPartnerType.html',
                  {'collection': data, 'districtData': district,
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4],'data_definition':data_definition,
                   'College': (College)
                   }
                  )

#TO invite community Partner to the Application
@login_required()
def invitecommunityPartnerUser(request):
    form = CommunityPartnerUserInvite()
    community_partner_user_form = CommunityPartnerUserForm()
    commPartner = []
    for object in CommunityPartner.objects.order_by('name'):
        commPartner.append(object.name)

    if request.method == 'POST':
        form = CommunityPartnerUserInvite(request.POST)
        community_partner_user_form = CommunityPartnerUserForm(request.POST)
        if form.is_valid() and community_partner_user_form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_communitypartner = True
            new_user.is_active = False
            new_user.set_password(raw_password='Default')
            new_user.save()
            communitypartneruser = CommunityPartnerUser(
                community_partner=community_partner_user_form.cleaned_data['community_partner'], user=new_user)
            communitypartneruser.save()
            mail_subject = 'UNO-CPI Community Partner Registration'
            current_site = get_current_site(request)
            message = render_to_string('account/CommunityPartner_Invite_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = new_user.email
            email = EmailMessage(mail_subject, message,to=[to_email])
            email.send()
            return render(request, 'home/communityuser_register_done.html', )
    return render(request, 'home/registration/inviteCommunityPartner.html' , {'form':form ,
                                                                              'community_partner_user_form':community_partner_user_form})

def registerCommPartner(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User,pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'home/registration/registerCommunityPartner.html', {'user': user})
    else:
        return render(request, 'home/registration/register_fail.html')



def commPartnerResetPassword(request,pk):
    if request.method == 'POST':
        user_obj = User.objects.get(pk=pk)
        form = SetPasswordForm(user_obj, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request,'home/registration/communityPartnerRegistrationComplete.html')
        else:
            return render(request, 'registration/password_reset_confirm.html', {'form': form, 'validlink': True })
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'registration/password_reset_confirm.html', {'form': form,'validlink':True })



#Issue Address Analysis Chart

def issueaddress(request):

    missions =[]
    for m in  MissionArea.objects.all():
        res={'id':m.id,'name':m.mission_name}
        missions.append(res)
    missions=sorted(missions,key=lambda i:i['name'])
    # print("sorted mission list",missions)
    missionarealist = list()
    for m in missions:
        missionarealist.append(m['name'])
    # print("mission_area1",mission_area1)
    subcategory = []
    y=[]
    # for x in ProjectSubCategory.objects.values('sub_category_id'):
    #    if (x["sub_category_id"] not in y):
    #     y.append(x["sub_category_id"])
    #
    # print(" ProjectSubCategory.objects.values_list('sub_category_id'):",y)
    # # for  x in ProjectSubCategory.objects.values_list('sub_category_id'):
    # #      y=[p.id for p in (SubCategory.objects.filter(id=x))]
    # # print("y value",y)


    data_definition = DataDefinition.objects.all()
    json_data=[]
    from_json_data=[]
    to_json_data=[]

    yrs = []
    yrid=[]
    acad_years = AcademicYear.objects.all()
    for e in acad_years:
        yrs.append(e.academic_year)
        yrid.append(e.id)
    max_yr_id = max(yrid)
    min_yr_id = min(yrid)
    # max_yr= [p.academic_year for p in (AcademicYear.objects.filter(id=max_yr_id))]
    max_year=yrs[len(yrs)-1]
    # min_yr = [p.academic_year for p in (AcademicYear.objects.filter(id=(max_yr_id-1)))]
    min_year=yrs[len(yrs)-2]
    # print(" min yaer",min_year," ma yaer ",max_year)


    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_init_selection = "All"

    b = request.GET.get('academic_year', None)
    ba = request.GET.get('end_academic_year', None)

    if ((b == '' or b == None) and (ba == '' or ba == None)):
        start = max_yr_id - 1
        end = max_yr_id
    elif ((b == '' or b == None) and (ba != '')):
        start = min_yr_id
        end = ba
    elif ((ba == '' or ba == None) and (b != '')):
        end = max_yr_id
        start = b
    else:
        start = b
        end = ba
    start = int(start)
    end = int(end)


    from_project_filter = FromProjectFilter(request.GET, queryset=Project.objects.filter())
    from_start = list(range(min_yr_id, (start + 1)))
    from_end = list(range(start, (max_yr_id + 1)))

    to_project_filter = ToProjectFilter(request.GET, queryset=Project.objects.all())
    to_start = list(range(min_yr_id, (end + 1)))
    to_end = list(range(end, (max_yr_id + 1)))

    from_project_count_data = list()
    to_project_count_data = list()
    from_subcat_count=list()
    to_subcat_count=list()
    subdrill = []
    from_subcat_counts=[]
    to_subcat_counts=[]




    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    college_filtered_ids = [campus.id for campus in college_filter.qs]

    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=college_filtered_ids))
    campus_project_filter_ids = [project.project_name_id for project in campus_project_filter.qs]

    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    projects = Project.objects.all()
    project_filtered_ids = [project.id for project in projects]

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    community_filtered_ids = [community.id for community in communityPartners.qs]


    comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
        community_partner_id__in=community_filtered_ids))
    comm_proj_filtered_ids = [project.project_name_id for project in comm_filter.qs]

    legislative_choices = []
    legislative_search = ''
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        # project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
            legislative_district=legislative_search))
        # project_filter = ProjectFilter(request.GET,
        #                                queryset=Project.objects.filter(legislative_district=legislative_search))


    proj1_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
    proj2_ids = list(set(campus_project_filter_ids).intersection(proj1_ids))
    project_ids = list(set(proj2_ids).intersection(comm_proj_filtered_ids))

    a = request.GET.get('engagement_type', None)
    c = request.GET.get('campus_partner', None)
    d = request.GET.get('college_name', None)
    # b = request.GET.get('academic_year', None)
    # ba = request.GET.get('end_academic_year', None)
    e = request.GET.get('community_type', None)
    f = request.GET.get('weitz_cec_part', None)

    if a is None or a == "All" or a == '':
        if b is None or b == "All" or b == '':
            if ba is None or ba == "All" or ba == '':
                if c is None or c == "All" or c == '':
                    if d is None or d == "All" or d == '':
                        if f is None or f == "All" or f == '':
                            if e is None or e == "All" or e == '':
                                project_ids = project_filtered_ids

    secondary_y_axis=[]
    Yaxis=[]
    for m in missions:
            y=[]
            subcategory=[]
            for s in MissionSubCategory.objects.filter(secondary_mission_area_id=m["id"]).values("sub_category_id"):
                if (s["sub_category_id"] not in y):
                    y.append(s["sub_category_id"])
            # print(" sub category ids for mission 1", y)
            for sc in SubCategory.objects.filter(id__in=y):
                res = {'id': sc.id, 'name': sc.sub_category}
                subcategory.append(res)
            subcategory = sorted(subcategory, key=lambda i: i['name'])
            subcategorylist = []
            for sc in subcategory:
                subcategorylist.append(sc['name'])
            mid = next((index for (index, d) in enumerate(missions) if d["name"] == m['name']),None)
            if f is None or f == "All" or f == '':
                if e is None or e == "All" or e == '':
                    project_ids = proj2_ids
            project_count1 = Project.objects.filter(academic_year__in=from_start).filter(end_academic_year=None).filter(id__in=project_ids)
            project_count2 = Project.objects.filter(academic_year__in=from_start).filter(end_academic_year__in=from_end).filter(id__in=project_ids)
            project_count3 = project_count1 | project_count2
            from_project_ids = []
            for c in project_count3:
                from_project_ids.append (c.id)
            from_project_count_ids = ProjectMission.objects.filter(mission=m['id']).filter(mission_type='Primary').filter(project_name_id__in=from_project_ids)
            from_project_count = ProjectMission.objects.filter(mission=m['id']).filter(mission_type='Primary').filter(
                project_name_id__in=from_project_ids).count()

            project_count4 = Project.objects.filter(academic_year__in=to_start).filter(end_academic_year=None).filter(id__in=project_ids)
            project_count5 = Project.objects.filter(academic_year__in=to_start).filter(end_academic_year__in=to_end).filter(id__in=project_ids)
            project_count6 = project_count4 | project_count5
            to_project_ids = []
            for c in project_count6:
                to_project_ids.append (c.id)
            to_project_count_ids = ProjectMission.objects.filter(mission=m['id']).filter(mission_type='Primary').filter(project_name_id__in=to_project_ids)
            to_project_count = ProjectMission.objects.filter(mission=m['id']).filter(mission_type='Primary').filter(
                project_name_id__in=to_project_ids).count()
            x=[pm.project_name_id for pm in from_project_count_ids]
            y = [pm.project_name_id for pm in to_project_count_ids]

            drilldata=[]
            if request.user.is_superuser:
                for sc in subcategory:
                    sid = next((index for (index, d) in enumerate(subcategory) if d["name"] == sc['name']), None)
                    from_project_mission_sub_ids=ProjectSubCategory.objects.filter(project_name_id__in=x).filter(sub_category_id=sc['id']).count()
                    to_project_mission_sub_ids = ProjectSubCategory.objects.filter(project_name_id__in=y).filter(
                        sub_category_id=sc['id']).count()
                    from_subcat_counts.append(from_project_mission_sub_ids)
                    to_subcat_counts.append(to_project_mission_sub_ids)
                    if(from_project_mission_sub_ids>to_project_mission_sub_ids):
                        drill = {"name":sc['name'],"x": from_project_mission_sub_ids,
                             "x2": to_project_mission_sub_ids, "y": sid ,"color":"red"}
                    else:
                        drill = {"name":sc['name'],"x": from_project_mission_sub_ids,
                                 "x2": to_project_mission_sub_ids, "y":sid ,"color":"turquoise"}
                    drilldata.append(drill)
                drilled = {"type":"xrange","name": m['name'], "id": m['name'], "yAxis": mid+1 ,"data": drilldata}
                subdrill.append(drilled)
            from_project_count_data.append(from_project_count)
            to_project_count_data.append(to_project_count)
            if(from_project_count > to_project_count):
                res = {"name":m['name'],"x": from_project_count, "x2": to_project_count, "y":mid, "drilldown":m['name'],"color":"red"}
            else:
                res = {"name": m['name'], "x": from_project_count, "x2": to_project_count, "y": mid ,
                       "drilldown": m['name'], "color": "turquoise"}
            resfrom = {"x": from_project_count,"y":mid,"drilldown":m['name']}
            resto = {"x": to_project_count,"y":mid,"drilldown":m['name']}

            json_data.append(res)
            from_json_data.append(resfrom)
            to_json_data.append(resto)
            # print(" mid value ",mid," lemngt ",len(missions))
            yaxis={
            'id':mid+1,
            'type': 'category',
            # 'min':1,
            # 'max':len(subcategorylist)-1,
            # 'tickInterval':1.0,
            'title': {'text': '',
                      'style': {'fontWeight': 'bold', 'color': 'black', 'fontSize': '15px'}},
            'labels': {'style': {'color': 'black', 'fontSize': '13px'}},
            'categories': subcategorylist}
            if(mid== len(missions)-1):
                yaxis = {
                    'id': mid + 1,
                    'type': 'category',
                    # 'min':1,
                    # 'max':len(subcategorylist)-1,
                    # 'tickInterval':1.0,
                    'title': {'text': 'Focus Area',
                              'style': {'fontWeight': 'bold', 'color': 'black', 'fontSize': '15px'}},
                    'labels': {'style': {'color': 'black', 'fontSize': '13px'}},
                    'categories': subcategorylist}
            secondary_y_axis.append(yaxis)

    primary_axis={  # Primary Axis for Mission Areas
                'id':0,
                'type': 'category',
                'title': {'text': '',
                          'style': {'fontWeight': 'bold', 'color': 'black', 'fontSize': '15px'}},
                'labels': {'style': {'color': 'black', 'fontSize': '13px'}},
                'categories': missionarealist,
            }
    Yaxis.append(primary_axis)
    for axis in secondary_y_axis:
        if(axis not in Yaxis):
            Yaxis.append(axis)

    # print(" yxis value in category ",Yaxis)
    Academic_Year = {
        'name': 'Analysis Start Year',
        'data': from_json_data,
        'color': 'teal',
        'type': 'scatter'}
    End_Academic_Year = {
        'name': 'Analysis Comparison (End) Year',
        'data': to_json_data,
        'color': 'blue',
        'type': 'scatter'}
    project_over_academic_years = {
        'name': 'No of Projects ',
        'data': json_data,
        'type':'xrange',
        'showInLegend':False,
        'marker':{
            'enabled':True
        }
        # 'color': 'turquoise'
                }


    dumbellchart = {

       'title': '',
        'xAxis': {'allowDecimals': False, 'title': {'text': 'Projects ',
                                                    'style': {'fontWeight': 'bold', 'color': 'black',
                                                              'fontSize': '15px'}}},
        'yAxis':Yaxis,
        'plotOptions': {
            'xrange': {
                'pointWidth': 4,
                'dataLabels': {
                    'enabled': True,
                    'inside':False,
                    'style': {
                        'fontSize': '6px'
                    },
                    'marker':{
                    'linewidth':'4px',
                    }

                },'colorByPoint': False,
                'tooltip': {
                    'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    'pointFormat': '<span style="color:{point.color}">{point.name}</span><br> FromYearProjectCount:{point.x}<br>ToYearProjectCount:{point.x2}<br>'
                }
            },

            'scatter': {
                'marker': {
                    'radius': 6,
                    'symbol': 'circle'
                }
            }
        },
        'tooltip': {
        'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
        'pointFormat': '<span style="color:{point.color}">{point.name}</span><br> ProjectCount:{point.x}<span></span> '
                 },
        'legend': {
            'layout': 'horizontal',
            'align': 'right',
            'verticalAlign': 'top',
            'x': -10,
            'y': 10,
            'borderWidth': 1,
            'backgroundColor': '#FFFFFF',
            'shadow': 'true'
        },


        'series': [project_over_academic_years, Academic_Year, End_Academic_Year],
        'drilldown':{
            'series': subdrill,
        }

    }
    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)
    engagement_type=request.GET.get('engagement_type',None)
    if engagement_type is None or engagement_type == "All" or engagement_type == '':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(engagement_type=engagement_type)

    dump = json.dumps(dumbellchart)
    return render(request, 'charts/issueaddressanalysis.html',
                      {'dumbellchart': dump, 'from_project_filter': from_project_filter,'project_filter':project_filter,
                       'to_project_filter': to_project_filter,
                       'data_definition': data_definition,
                       'campus_filter': campus_filter, 'communityPartners': communityPartners,
                       'college_filter': college_filter, 'campus_id': campus_id,'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                        'max_year':max_year,'min_year':min_year,'cec_part_choices': cec_part_choices})





##### Get the Chart JSONS for network Analysis ##############
def chartjsons():
    # with open('home/static/GEOJSON/ID2.geojson') as f:
    #     geojson = json.load(f)
    #
    # district = geojson["features"]
    campus_partner=open('home/static/charts_json/campus_partners.json')
    # campus_partner_json=json.load(charts_campuses)
    campus_partner_json = json.load(campus_partner)#local
    community_partner = open('home/static/charts_json/community_partners.json')
    # community_partner_json = json.load(charts_communities)
    community_partner_json = json.load(community_partner)#local
    mission_subcategories = open('home/static/charts_json/mission_subcategories.json')
    # mission_subcategories_json = json.load(charts_missions)
    mission_subcategories_json = json.load(mission_subcategories)#local
    projects =open ('home/static/charts_json/projects.json')
    # projects_json = json.load(charts_projects)
    projects_json = json.load(projects)#local
    return (campus_partner_json,community_partner_json,mission_subcategories_json,projects_json)



###Network Analysis Chart
def networkanalysis(request):
    data_definition = DataDefinition.objects.all()
    Campuspartner = GEOJSON2()[4]
    Communitypartner = GEOJSON2()[3]
    data = GEOJSON2()[0]
    campus_partner_json=chartjsons()[0]
    community_partner_json=chartjsons()[1]
    mission_subcategories_json=chartjsons()[2]
    projects_json=chartjsons()[3]
    yrs = []
    acad_years = AcademicYear.objects.all()
    for e in acad_years:
        yrs.append(e.id)
    max_yr_id = max(yrs)
    max_yr = [p.academic_year for p in (AcademicYear.objects.filter(id=max_yr_id))]
    max_year = max_yr[0]

    mission = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.order_by('academic_year'))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # campus_partner_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    # print("campus_partner_filter",campus_filter)
    k12_selection = request.GET.get('k12_flag', None)
    k12_init_selection = "All"
    if k12_selection is None:
        k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    if k12_selection == 'Yes':
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True))

    elif k12_selection == 'No':
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False))

    # else:
    #     project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)




    return render(request, 'charts/network.html',
                  { 'Missionlist': sorted(GEOJSON2()[2]),'data_definition':data_definition,'Collegenames': (GEOJSON2()[7]),
                   'campus_partner_json':campus_partner_json,'community_partner_json':community_partner_json,'max_yr_id':max_yr_id,'max_year':max_year,
                   'mission_subcategories_json':mission_subcategories_json,'projects_json':projects_json,
                    'project_filter': project_filter,'campus_filter': campus_filter,'missions': mission,'communityPartners': communityPartners,
                    'college_filter': college_filter,'k12_choices': k12_choices,'campus_id': campus_id} )

