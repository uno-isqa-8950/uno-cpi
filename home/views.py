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
from django.utils.http import url_has_allowed_host_and_scheme
from .tokens import account_activation_token
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.mail import EmailMessage
from collections import OrderedDict
import sys
import xlrd
from django.utils import timezone
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
from projects.models import AcademicYear, EngagementType

sql=sqlfiles
logger = logging.getLogger(__name__)
#writing into amazon s3 bucket
ACCESS_ID=settings.AWS_ACCESS_KEY_ID
ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
s3 = boto3.resource('s3',
         aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= ACCESS_KEY)

# Read JSON files for charts

# charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
# charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
# charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
# charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
# charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
# charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
# charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
# charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')

#read Partner.geojson from s3
#content_object_partner = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Partner.geojson')
#partner_geojson = content_object_partner.get()['Body'].read().decode('utf-8')

#read Project.geojson from s3
#content_object_project = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Project.geojson')
#project_geojson = content_object_project.get()['Body'].read().decode('utf-8')

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

def resourceData(request):
    resources = Resource.objects.filter(isAccessible=1).order_by('listing_order')
    return {'resources': resources}

def home(request):
    return render(request, 'home/communityPartner.html',
                  {'home': home})


def MapHome(request):
    return render(request, 'home/Map_Home.html',
                  {'MapHome': MapHome})

def thanks(request):
    return render(request, 'home/thanks.html')


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
            new_user.is_active = True
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
                'uid': url_has_allowed_host_and_scheme(force_bytes(new_user.pk)).decode(),
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
        uid = force_str(url_has_allowed_host_and_scheme(uidb64))
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


# (14) Primary Focus Area with Topics Details  Report: - new focus areas report logic
def primary_focus_topic_info(request):
    data_definition = DataDefinition.objects.all()
    data_list =[]
    rpt_total_comm_partners = 0
    rpt_total_camp_partners = 0
    rpt_total_projects = 0
    rpt_total_uno_students = 0
    rpt_total_uno_hours = 0
    rpt_total_k12_students = 0
    rpt_total_k12_hours = 0
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_filter_qs = CampusPartner.objects.all()
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]
    # campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())

    engagement_filter_qs = EngagementType.objects.all()
    eng_project_filter = [{'name': e.name, 'id': e.id} for e in engagement_filter_qs]

    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()

    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]


    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter


    academic_year_filter = request.GET.get('academic_year', None)
    acad_years = AcademicYear.objects.all()
    yrs =[]
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if month > 7:
        a_year = str(year-1) + "-" + str(year )[-2:]
    else:
        a_year = str(year - 2) + "-" + str(year-1)[-2:]

    for e in acad_years:
        yrs.append(e.id)
    try:
        acad_year = AcademicYear.objects.get(academic_year=a_year).id
        default_yr_id = acad_year - 1
    except AcademicYear.DoesNotExist:
        default_yr_id = max(yrs)
    max_yr_id = max(yrs)


    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(default_yr_id)
        academic_end_year_cond = int(default_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = -1
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': "All"})

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        #cec_part_selection = cec_part_init_selection
        cec_comm_part_cond = '%'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "CURR_COMM":
        cec_comm_part_cond = 'Current'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_COMM":
        cec_comm_part_cond = 'Former'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Former'

    elif cec_part_selection == "CURR_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Current'

    engagement_filter = request.GET.get('engagement_type', None)
    if engagement_filter is None or engagement_filter == "All" or engagement_filter == '':
        engagement_cond = '%'
        engagement_id = -1
    else:
        engagement_cond = engagement_filter
        engagement_id = int(engagement_filter)

    params = [mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond, engagement_cond,
              academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond,
              mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond, engagement_cond,
              academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.primaryFocusTopic_report_sql, params)

    #cec_part_choices = CecPartChoiceForm()
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})


    for obj in cursor.fetchall():
        comm_ids = obj[12]

        proj_ids = obj[10]

        proj_idList = ''
        comm_idList = ''

        if proj_ids is not None:
            if None in proj_ids:
                proj_ids.pop(-1)

            name_count = 0
            if len(proj_ids) > 0:
                for i in proj_ids:
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        if comm_ids is not None:
            if None in comm_ids:
                comm_ids.pop(-1)

            name_count = 0
            if len(comm_ids) > 0:
                for i in comm_ids:
                    comm_idList = comm_idList + str(i)
                    if name_count < len(comm_ids) - 1:
                        comm_idList = comm_idList + str(",")
                        name_count = name_count + 1

        if obj[0] == 'Focus':
            rpt_total_comm_partners += obj[11]
            rpt_total_camp_partners += obj[13]
            rpt_total_projects += obj[9]
            rpt_total_uno_students += obj[14]
            rpt_total_uno_hours += obj[15]
            rpt_total_k12_students += obj[16]
            rpt_total_k12_hours += obj[17]

        data_list.append({"rec_type": obj[0], "focus_id": obj[1],
                          "focus_name": obj[2], "focus_desc": obj[3],
                          "focus_image": obj[4], "focus_color": obj[5],
                          "topic_id": obj[6], "topic_name": obj[7], "topic_desc": obj[8],
                          "project_count": obj[9],  "project_id_array": obj[10], "proj_id_list": proj_idList,
                          "community_count": obj[11], "comm_id_array": obj[12],
                          "comm_id_list": comm_idList, "campus_count": obj[13],
                          "total_uno_students": obj[14], "total_uno_hours": obj[15],
                          "total_k12_students": obj[16], "total_k12_hours": obj[17]})

    #print('data_list: ' + str(data_list))

    return render(request, 'reports/ProjectFocusTopicInfo.html',
                   {'college_filter': college_filter, 'missions_filter': missions_filter,
                    'engagement_filter': eng_project_filter, 'engagement_id': engagement_id,
                    'year_filter': year_filter, 'focus_topic_list': data_list,
                    'data_definition':data_definition, 'communityPartners' : communityPartners ,
                    'campus_filter': campus_project_filter, 'campus_id': campus_id, 'cec_part_choices': cec_part_choices,
                    'rpt_total_comm_partners': rpt_total_comm_partners, 'rpt_total_camp_partners': rpt_total_camp_partners,
                    'rpt_total_projects': rpt_total_projects,
                    'rpt_total_uno_students': rpt_total_uno_students, 'rpt_total_uno_hours': rpt_total_uno_hours,
                    'rpt_total_k12_students': rpt_total_k12_students, 'rpt_total_k12_hours': rpt_total_k12_hours})


def project_partner_info_public(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    proj_total = 0
    comm_total = 0
    students_total = 0
    hours_total = 0
    camp_total = 0
    k12_stu_total = 0
    k12_hr_total = 0
    data_list = []

    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_filter_qs = CampusPartner.objects.all()
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]
    college_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    academic_year_filter = request.GET.get('academic_year', None)
    acad_years = AcademicYear.objects.all()
    yrs = []
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if month > 7:
        a_year = str(year - 1) + "-" + str(year)[-2:]
    else:
        a_year = str(year - 2) + "-" + str(year - 1)[-2:]

    for e in acad_years:
        yrs.append(e.id)
    try:
        acad_year = AcademicYear.objects.get(academic_year=a_year).id
        default_yr_id = acad_year
    except AcademicYear.DoesNotExist:
        default_yr_id = max(yrs)
    max_yr_id = max(yrs)

    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(default_yr_id)
        academic_end_year_cond = int(default_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = -1
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': "All"})

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        # cec_part_selection = cec_part_init_selection
        cec_comm_part_cond = '%'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "CURR_COMM":
        cec_comm_part_cond = 'Current'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_COMM":
        cec_comm_part_cond = 'Former'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Former'

    elif cec_part_selection == "CURR_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Current'

    cursor = connection.cursor()
    project_start = "with mission_filter as (select pm.mission_id mission_id \
                  , count(distinct p.project_name) Projects \
                  , array_agg(distinct p.id) projects_id \
                  , count(distinct pcamp.campus_partner_id) CampPartners \
                   from projects_project p \
                   left join projects_projectcampuspartner pcamp on p.id = pcamp.project_name_id \
                   left join projects_status s on  p.status_id = s.id \
                   left join projects_projectmission pm on p.id = pm.project_name_id  and lower(pm.mission_type) = 'primary' \
                   left join partners_campuspartner c on pcamp.campus_partner_id = c.id  \
				   left join projects_projectcommunitypartner pcp on pcp.project_name_id = p.id \
                   left join partners_communitypartner cp on cp.id = pcp.community_partner_id \
                   where  s.name != 'Drafts'  and " \
                "((p.academic_year_id <=" + str(academic_start_year_cond) + ") AND \
                            (COALESCE(p.end_academic_year_id, p.academic_year_id) >=" + str(academic_end_year_cond) + "))"

    project_clause_query = " "
    community_clause_query = " "

    if eng_type_cond != '%':
        project_clause_query += " and p.engagement_type_id::text like '" + eng_type_cond + "'"
        community_clause_query += " and p.engagement_type_id::text like '" + eng_type_cond + "'"

    if campus_partner_cond != '%':
        project_clause_query += " and pcamp.campus_partner_id::text like '" + campus_partner_cond + "'"
        community_clause_query += " and pcamp.campus_partner_id::text like '" + campus_partner_cond + "'"

    if college_unit_cond != '%':
        project_clause_query += " and c.college_name_id::text like '" + college_unit_cond + "'"
        community_clause_query += " and c.college_name_id::text like '" + college_unit_cond + "'"

    if cec_camp_part_cond != '%':
        project_clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '" + cec_camp_part_cond + "')"
        community_clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '" + cec_camp_part_cond + "')"

    if community_type_cond != '%':
        project_clause_query += " and cp.community_type_id::text like '" + community_type_cond + "'"
        community_clause_query += " and cp.community_type_id::text like '" + community_type_cond + "'"

    if cec_comm_part_cond != '%':
        project_clause_query += " and  cp.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '" + cec_comm_part_cond + "')"
        community_clause_query += " and  cp.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '" + cec_comm_part_cond + "')"


    peoject_query_end = project_start + project_clause_query + " group by mission_id \
                                                                order by mission_id),"

    community_start = "mission_comm_filter as (select CommMission.mission_area_id mission_id \
			        , count(distinct pcp.community_partner_id) CommParnters \
                    , array_agg(distinct pcp.community_partner_id) comms_id \
                    from projects_projectcommunitypartner pcp \
                    left join projects_project p on p.id = pcp.project_name_id \
                    left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pcp.community_partner_id and  CommMission.mission_type='Primary' \
                    left join partners_communitypartner cp on cp.id = pcp.community_partner_id \
                    left join projects_projectcampuspartner pcamp on p.id = pcamp.project_name_id \
                    left join partners_campuspartner c on pcamp.campus_partner_id = c.id \
                    left join projects_status s on  p.status_id = s.id \
                    where s.name != 'Drafts' \
                    and ((p.academic_year_id <=" + str(academic_start_year_cond) + ") AND \
                        (COALESCE(p.end_academic_year_id, p.academic_year_id) >=" + str(academic_end_year_cond) + "))"

    query_end = peoject_query_end + community_start + community_clause_query + " group by mission_id \
					order by mission_id) \
                    Select hm.mission_name mission_area \
                    , hm.description description \
                    , COALESCE(mission_filter.Projects, 0) proj \
                    , mission_filter.projects_id proj_ids \
                    , COALESCE(mission_filter.CampPartners, 0) camp \
                    , COALESCE(mission_comm_filter.CommParnters, 0) comm \
                    , mission_comm_filter.comms_id comm_ids \
                    , hm.mission_color color \
                    from home_missionarea hm \
                    left join mission_filter on hm.id = mission_filter.mission_id \
                    left join mission_comm_filter on hm.id = mission_comm_filter.mission_id \
                    group by mission_area, description, proj, proj_ids, camp, comm, comm_ids, color \
                    order by mission_area;"


    cursor.execute(query_end)
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    for obj in cursor.fetchall():
        proj_ids = obj[3]
        comm_ids = obj[6]
        proj_idList = ''
        comm_idList = ''
        sum_uno_students = 0
        sum_uno_hours = 0
        sum_k12_students = 0
        sum_k12_hours = 0
        if proj_ids is not None:
            name_count = 0
            if None in proj_ids:
                proj_ids.pop(-1)

            if len(proj_ids) > 0:
                for i in proj_ids:
                    cursor.execute("Select p.total_uno_students , p.total_uno_hours, p.total_k12_students, p.total_k12_hours from projects_project p where p.id=" + str(i))
                    for obj1 in cursor.fetchall():
                        sum_uno_students = sum_uno_students + obj1[0]
                        sum_uno_hours = sum_uno_hours + obj1[1]
                        sum_k12_students = sum_k12_students + obj1[2]
                        sum_k12_hours = sum_k12_hours + obj1[3]
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        if comm_ids is not None:
            name_count = 0
            if None in comm_ids:
                comm_ids.pop(-1)

            if len(comm_ids) > 0:
                for i in comm_ids:
                    comm_idList = comm_idList + str(i)
                    if name_count < len(comm_ids) - 1:
                        comm_idList = comm_idList + str(",")
                        name_count = name_count + 1

        data_list.append({"mission_name": obj[0], "description": obj[1], "project_count": obj[2], "project_id_list": proj_idList,
                            "campus_count": obj[4], "community_count": obj[5], "comm_id_list": comm_idList,
                            "total_uno_students": sum_uno_students, "total_uno_hours": sum_uno_hours,
                          "sum_k12_students": sum_k12_students, "sum_k12_hours": sum_k12_hours, 'focus_color': obj[7]})

        proj_total = proj_total + obj[2]
        comm_total = comm_total + obj[5]
        students_total = students_total + sum_uno_students
        hours_total = hours_total + sum_uno_hours
        camp_total = camp_total + obj[4]
        k12_stu_total = k12_stu_total + sum_k12_students
        k12_hr_total = k12_hr_total + sum_k12_hours

    return render(request, 'reports/ProjectPartnerInfo_public.html',
              { 'project_filter': project_filter, 'data_definition': data_definition, 'cec_part_choices': cec_part_choices,
               'year_filter': year_filter, 'communityPartners': communityPartners, 'mission_list': data_list,
               'campus_filter': campus_project_filter, 'college_filter': college_partner_filter,'campus_id': campus_id,
               'proj_total': proj_total, 'comm_total': comm_total, 'students_total': students_total,
               'camp_total' : camp_total, 'k12_stu_total': k12_stu_total, 'k12_hr_total': k12_hr_total,'hours_total': hours_total} )


def project_partner_info_admin(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    proj_total = 0
    comm_total = 0
    students_total = 0
    hours_total = 0
    camp_total = 0
    k12_stu_total = 0
    k12_hr_total = 0
    data_list = []

    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_filter_qs = CampusPartner.objects.all()
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]
    college_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    academic_year_filter = request.GET.get('academic_year', None)
    acad_years = AcademicYear.objects.all()
    yrs = []
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if month > 7:
        a_year = str(year - 1) + "-" + str(year)[-2:]
    else:
        a_year = str(year - 2) + "-" + str(year - 1)[-2:]

    for e in acad_years:
        yrs.append(e.id)
    try:
        acad_year = AcademicYear.objects.get(academic_year=a_year).id
        default_yr_id = acad_year
    except AcademicYear.DoesNotExist:
        default_yr_id = max(yrs)
    max_yr_id = max(yrs)

    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(default_yr_id)
        academic_end_year_cond = int(default_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = -1
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': "All"})

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        # cec_part_selection = cec_part_init_selection
        cec_comm_part_cond = '%'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "CURR_COMM":
        cec_comm_part_cond = 'Current'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_COMM":
        cec_comm_part_cond = 'Former'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Former'

    elif cec_part_selection == "CURR_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Current'

    cursor = connection.cursor()
    project_start = "with mission_filter as (select pm.mission_id mission_id \
                  , count(distinct p.project_name) Projects \
                  , array_agg(distinct p.id) projects_id \
                  , count(distinct pcamp.campus_partner_id) CampPartners \
                   from projects_project p \
                   left join projects_projectcampuspartner pcamp on p.id = pcamp.project_name_id \
                   left join projects_status s on  p.status_id = s.id \
                   left join projects_projectmission pm on p.id = pm.project_name_id  and lower(pm.mission_type) = 'primary' \
                   left join partners_campuspartner c on pcamp.campus_partner_id = c.id  \
				   left join projects_projectcommunitypartner pcp on pcp.project_name_id = p.id \
                   left join partners_communitypartner cp on cp.id = pcp.community_partner_id \
                   where  s.name != 'Drafts'  and " \
                    "((p.academic_year_id <=" + str(academic_start_year_cond) + ") AND \
                            (COALESCE(p.end_academic_year_id, p.academic_year_id) >=" + str(
        academic_end_year_cond) + "))"

    project_clause_query = " "
    community_clause_query = " "
    subCat_clause_query = " "


    if eng_type_cond != '%':
        project_clause_query += " and p.engagement_type_id::text like '" + eng_type_cond + "'"
        community_clause_query += " and p.engagement_type_id::text like '" + eng_type_cond + "'"
        subCat_clause_query += " and p.engagement_type_id::text like '" + eng_type_cond + "'"

    if campus_partner_cond != '%':
        project_clause_query += " and pcamp.campus_partner_id::text like '" + campus_partner_cond + "'"
        community_clause_query += " and pcamp.campus_partner_id::text like '" + campus_partner_cond + "'"
        subCat_clause_query += " and pcamp.campus_partner_id::text like '" + campus_partner_cond + "'"

    if college_unit_cond != '%':
        project_clause_query += " and c.college_name_id::text like '" + college_unit_cond + "'"
        community_clause_query += " and c.college_name_id::text like '" + college_unit_cond + "'"
        subCat_clause_query += " and c.college_name_id::text like '" + college_unit_cond + "'"

    if cec_camp_part_cond != '%':
        project_clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '" + cec_camp_part_cond + "')"
        community_clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '" + cec_camp_part_cond + "')"
        subCat_clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '" + cec_camp_part_cond + "')"

    if community_type_cond != '%':
        project_clause_query += " and cp.community_type_id::text like '" + community_type_cond + "'"
        community_clause_query += " and cp.community_type_id::text like '" + community_type_cond + "'"
        subCat_clause_query += " and comm.community_type_id::text like '" + community_type_cond + "'"

    if cec_comm_part_cond != '%':
        project_clause_query += " and  cp.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '" + cec_comm_part_cond + "')"
        community_clause_query += " and  cp.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '" + cec_comm_part_cond + "')"
        subCat_clause_query += " and  comm.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '" + cec_comm_part_cond + "')"

    peoject_query_end = project_start + project_clause_query + " group by mission_id \
                                                                order by mission_id),"

    community_start = "mission_comm_filter as (select CommMission.mission_area_id mission_id \
			        , count(distinct pcp.community_partner_id) CommParnters \
                    , array_agg(distinct pcp.community_partner_id) comms_id \
                    from projects_projectcommunitypartner pcp \
                    left join projects_project p on p.id = pcp.project_name_id \
                    left join partners_communitypartnermission CommMission on CommMission.community_partner_id = pcp.community_partner_id and  CommMission.mission_type='Primary' \
                    left join partners_communitypartner cp on cp.id = pcp.community_partner_id \
                    left join projects_projectcampuspartner pcamp on p.id = pcamp.project_name_id \
                    left join partners_campuspartner c on pcamp.campus_partner_id = c.id \
                    left join projects_status s on  p.status_id = s.id \
                    where s.name != 'Drafts' \
                    and ((p.academic_year_id <=" + str(academic_start_year_cond) + ") AND \
                        (COALESCE(p.end_academic_year_id, p.academic_year_id) >=" + str(academic_end_year_cond) + "))"

    query_end = peoject_query_end + community_start + community_clause_query + " group by mission_id \
					order by mission_id) \
                    Select hm.mission_name mission_area \
                    , hm.description description \
                    , COALESCE(mission_filter.Projects, 0) proj \
                    , mission_filter.projects_id proj_ids \
                    , COALESCE(mission_filter.CampPartners, 0) camp \
                    , COALESCE(mission_comm_filter.CommParnters, 0) comm \
                    , mission_comm_filter.comms_id comm_ids \
                    , hm.mission_color color \
					, hm.id mission_ids \
                    from home_missionarea hm \
                    left join mission_filter on hm.id = mission_filter.mission_id \
                    left join mission_comm_filter on hm.id = mission_comm_filter.mission_id \
                    group by mission_area, description, proj, proj_ids, camp, comm, comm_ids, color, mission_ids \
                    order by mission_area;"

    cursor.execute(query_end)
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    for obj in cursor.fetchall():
        proj_ids = obj[3]
        comm_ids = obj[6]
        mission_ids = obj[8]
        proj_idList = ''
        comm_idList = ''
        sum_uno_students = 0
        sum_uno_hours = 0
        sum_k12_students = 0
        sum_k12_hours = 0
        if proj_ids is not None:
            name_count = 0
            if None in proj_ids:
                proj_ids.pop(-1)

            if len(proj_ids) > 0:
                for i in proj_ids:
                    cursor.execute("Select p.total_uno_students , p.total_uno_hours, p.total_k12_students, p.total_k12_hours \
                                    from projects_project p where p.id=" + str(i))
                    for obj1 in cursor.fetchall():
                        sum_uno_students = sum_uno_students + obj1[0]
                        sum_uno_hours = sum_uno_hours + obj1[1]
                        sum_k12_students = sum_k12_students + obj1[2]
                        sum_k12_hours = sum_k12_hours + obj1[3]
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        
        if comm_ids is not None:
            name_count = 0
            if None in comm_ids:
                comm_ids.pop(-1)

            if len(comm_ids) > 0:
                for i in comm_ids:
                    comm_idList = comm_idList + str(i)
                    if name_count < len(comm_ids) - 1:
                        comm_idList = comm_idList + str(",")
                        name_count = name_count + 1


        sub_list = []
        subCat_start_query = "with sub_category_filter as (select psc.sub_category_id sub_cat_id, \
																		array_agg(distinct p.id) projects_id, \
																		count(distinct p.project_name) projects_count, \
																		count(distinct pcamp.campus_partner_id) camp_count \
																		from projects_missionsubcategory ms \
                    left join projects_projectsubcategory psc on psc.sub_category_id = ms.sub_category_id \
                    left join projects_subcategory sub on sub.id = psc.sub_category_id \
                    left join projects_project p on p.id = psc.project_name_id \
                    left join projects_projectcampuspartner pcamp on pcamp.project_name_id = p.id \
                    left join projects_projectcommunitypartner pcomm on pcomm.project_name_id = p.id \
                    left join partners_communitypartner comm on comm.id = pcomm.community_partner_id \
                    left join projects_status s on s.id = p.status_id \
                    left join partners_campuspartner c on pcamp.campus_partner_id = c.id \
                    where s.name !='Drafts' \
                          and ((p.academic_year_id <=" + str(academic_start_year_cond) + ") AND \
                              (COALESCE(p.end_academic_year_id, p.academic_year_id) >=" + str(academic_end_year_cond) + "))"

        subCat_query_end = subCat_start_query + subCat_clause_query + "group by sub_cat_id \
                                                                            order by sub_cat_id) \
                                                                            select distinct sub.sub_category sub_cat \
                                                                            , sub.sub_category_descr description \
                                                                            , scf.projects_id proj_ids \
                                                                            , COALESCE(scf.projects_count, 0) proj_counts \
                                                                            , COALESCE(scf.camp_count, 0) campus_counts \
                                                                            , ms.secondary_mission_area_id sec_mission \
                                                                            from projects_subcategory sub \
                                                                            left join projects_missionsubcategory ms on ms.sub_category_id = sub.id \
                                                                            left join sub_category_filter scf on sub.id = scf.sub_cat_id \
                                                                            where ms.secondary_mission_area_id = " + str(mission_ids) + \
                                                                            " group by sub_cat, description, proj_ids, proj_counts, campus_counts, sec_mission \
                                                                            order by sub_cat;"

        cursor.execute(subCat_query_end)
        for sub_obj in cursor.fetchall():
            sub_proj_ids = sub_obj[2]
            sub_proj_idList = ''
            sub_sum_uno_students = 0
            sub_sum_uno_hours = 0
            sub_sum_k12_students = 0
            sub_sum_k12_hours = 0
            if sub_proj_ids is not None:
                sub_name_count = 0
                if None in sub_proj_ids:
                    sub_proj_ids.pop(-1)
                if len(sub_proj_ids) > 0:
                    for ids in sub_proj_ids:
                        cursor.execute("Select p.total_uno_students , p.total_uno_hours, p.total_k12_students, p.total_k12_hours \
                                 from projects_project p where p.id=" + str(ids))
                        for obj_sum in cursor.fetchall():
                            sub_sum_uno_students = sub_sum_uno_students + obj_sum[0]
                            sub_sum_uno_hours = sub_sum_uno_hours + obj_sum[1]
                            sub_sum_k12_students = sub_sum_k12_students + obj_sum[2]
                            sub_sum_k12_hours = sub_sum_k12_hours + obj_sum[3]

                        sub_proj_idList = sub_proj_idList + str(ids)
                        if sub_name_count < len(sub_proj_ids) - 1:
                            sub_proj_idList = sub_proj_idList + str(",")
                            sub_name_count = sub_name_count + 1
            sub_list.append({"subCat": sub_obj[0], "sub_description": sub_obj[1], "sub_proj_ids": sub_proj_idList,
                                        "sub_project_count": sub_obj[3], "sub_camp_count": sub_obj[4], "sub_mission": sub_obj[5],
                                        "sub_sum_uno_students": sub_sum_uno_students, "sub_sum_uno_hours": sub_sum_uno_hours,
                                        "sub_sum_k12_students": sub_sum_k12_students, "sub_sum_k12_hours": sub_sum_k12_hours})

        data_list.append({"mission_name": obj[0], "description": obj[1], "project_count": obj[2], "project_id_list": proj_idList,
                    "campus_count": obj[4], "community_count": obj[5], "comm_id_list": comm_idList,
                    "total_uno_students": sum_uno_students, "total_uno_hours": sum_uno_hours, 'focus_color': obj[7],
                    "sum_k12_students": sum_k12_students, "sum_k12_hours": sum_k12_hours,
                    "mission_id": obj[8], "sub_category": sub_list})

        proj_total = proj_total + obj[2]
        comm_total = comm_total + obj[5]
        camp_total = camp_total + obj[4]
        k12_stu_total = k12_stu_total + sum_k12_students
        k12_hr_total = k12_hr_total + sum_k12_hours
        students_total = students_total + sum_uno_students
        hours_total = hours_total + sum_uno_hours

    return render(request, 'reports/ProjectPartnerInfo_admin.html',
              {'project_filter': project_filter, 'data_definition': data_definition,
               'cec_part_choices': cec_part_choices,
               'year_filter': year_filter, 'communityPartners': communityPartners, 'mission_list': data_list,
               'campus_filter': campus_project_filter, 'college_filter': college_partner_filter, 'campus_id': campus_id,
               'proj_total': proj_total, 'comm_total': comm_total, 'students_total': students_total,
               'camp_total' : camp_total, 'k12_stu_total': k12_stu_total, 'k12_hr_total': k12_hr_total, 'hours_total': hours_total})


def engagement_info(request):
    data_definition = DataDefinition.objects.all()
    data_list =[]
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_filter_qs = CampusPartner.objects.all()
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]
    college_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()

    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]


    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter


    academic_year_filter = request.GET.get('academic_year', None)
    acad_years = AcademicYear.objects.all()
    yrs =[]
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    if month > 7:
        a_year = str(year-1) + "-" + str(year )[-2:]
    else:
        a_year = str(year - 2) + "-" + str(year-1)[-2:]

    for e in acad_years:
        yrs.append(e.id)
    try:
        acad_year = AcademicYear.objects.get(academic_year=a_year).id
        default_yr_id = acad_year
    except AcademicYear.DoesNotExist:
        default_yr_id = max(yrs)
    max_yr_id = max(yrs)


    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(default_yr_id)
        academic_end_year_cond = int(default_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = -1
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': "All"})

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        #cec_part_selection = cec_part_init_selection
        cec_comm_part_cond = '%'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "CURR_COMM":
        cec_comm_part_cond = 'Current'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_COMM":
        cec_comm_part_cond = 'Former'
        cec_camp_part_cond = '%'

    elif cec_part_selection == "FORMER_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Former'

    elif cec_part_selection == "CURR_CAMP":
        cec_comm_part_cond = '%'
        cec_camp_part_cond = 'Current'

    # params = [community_type_cond, cec_comm_part_cond, mission_type_cond,  campus_partner_cond, college_unit_cond,
    #           academic_start_year_cond, academic_end_year_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    engagement_start = "with eng_type_filter as (select p.engagement_type_id eng_id \
                  , count(distinct p.project_name) Projects \
                  , array_agg(distinct p.id) projects_id \
                  , count(distinct pcomm.community_partner_id) CommPartners \
                  , array_agg(distinct pcomm.community_partner_id) CommPartners_id \
                  , count(distinct pcamp.campus_partner_id) CampPartners \
                   from projects_engagementtype e \
                   join projects_project p on p.engagement_type_id = e.id \
                   left join projects_projectcampuspartner pcamp on p.id = pcamp.project_name_id \
                   left join projects_projectcommunitypartner pcomm on p.id = pcomm.project_name_id \
                   left join partners_communitypartner comm on pcomm.community_partner_id = comm.id  \
                   left join projects_status s on  p.status_id = s.id \
                   join projects_projectmission pm on p.id = pm.project_name_id  and lower(pm.mission_type) = 'primary' \
                   left join partners_campuspartner c on pcamp.campus_partner_id = c.id  \
                   where  s.name != 'Drafts'  and " \
                       "((p.academic_year_id <="+ str(academic_start_year_cond)  +") AND \
                            (COALESCE(p.end_academic_year_id, p.academic_year_id) >="+str(academic_end_year_cond)+"))"
    clause_query=" "
    if mission_type_cond !='%':
        clause_query += " and pm.mission_id::text like '"+ mission_type_cond +"'"

    if campus_partner_cond !='%':
        clause_query +=" and pcamp.campus_partner_id::text like '"+ campus_partner_cond +"'"

    if college_unit_cond !='%':
        clause_query += " and c.college_name_id::text like '"+ college_unit_cond +"'"


    if cec_camp_part_cond != '%':
        clause_query += " and c.cec_partner_status_id in (select id from partners_cecpartnerstatus where name like '"+ cec_camp_part_cond +"')"

    if community_type_cond !='%':
        clause_query += " and comm.community_type_id::text like '"+ community_type_cond +"'"

    if cec_comm_part_cond != '%':
        clause_query +=  " and  comm.cec_partner_status_id in  (select id from partners_cecpartnerstatus where name like '"+ cec_comm_part_cond +"')"



    query_end = engagement_start + clause_query + " group by eng_id \
                order by eng_id) \
                Select distinct eng.name eng_type \
                      , eng.description eng_desc \
                     , COALESCE(eng_type_filter.Projects, 0) proj \
                     , eng_type_filter.projects_id proj_ids \
                     , COALESCE(eng_type_filter.CommPartners, 0) comm \
                     , eng_type_filter.CommPartners_id comm_id \
                     , COALESCE(eng_type_filter.CampPartners, 0) camp \
                 from projects_engagementtype eng \
                    left join eng_type_filter on eng.id = eng_type_filter.eng_id \
                group by eng_type, eng_desc, proj, proj_ids, comm, comm_id, camp \
                order by eng_type;"

    # cursor.execute(sql.engagement_types_report_sql, params)
    cursor.execute(query_end)
    #cec_part_choices = CecPartChoiceForm()
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    for obj in cursor.fetchall():
        comm_ids = obj[5]
        proj_ids = obj[3]
        proj_idList = ''
        comm_idList = ''
        sum_uno_students = 0
        sum_uno_hours = 0
        if proj_ids is not None:
            name_count = 0
            if None in proj_ids:
                proj_ids.pop(-1)
                
            if len(proj_ids) > 0:
                for i in proj_ids:
                    cursor.execute("Select p.total_uno_students , p.total_uno_hours from projects_project p where p.id="+ str(i))
                    for obj1 in cursor.fetchall():
                        sum_uno_students = sum_uno_students + obj1[0]
                        sum_uno_hours = sum_uno_hours + obj1[1]
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        if comm_ids is not None:
            name_count = 0
            if None in comm_ids:
                comm_ids.pop(-1)

            if len(comm_ids) > 0:
                for i in comm_ids:
                    comm_idList = comm_idList + str(i)
                    if name_count < len(comm_ids) - 1:
                        comm_idList = comm_idList + str(",")
                        name_count = name_count + 1

        data_list.append({"engagement_name": obj[0], "description": obj[1], "project_count": obj[2], "project_id_list": proj_idList,
                          "community_count": obj[4], "comm_id_list": comm_idList, "campus_count": obj[6], "total_uno_students": sum_uno_students,
                          "total_uno_hours": sum_uno_hours})


    return render(request, 'reports/EngagementTypeReport.html',
                   {'college_filter': college_partner_filter, 'missions_filter': missions_filter,
                    'year_filter': year_filter, 'engagement_List': data_list,
                    'data_definition':data_definition, 'communityPartners' : communityPartners ,
                    'campus_filter': campus_project_filter, 'campus_id':campus_id, 'cec_part_choices': cec_part_choices})


# Chart for projects with mission areas
@login_required()
def missionchart(request):
    data_definition = DataDefinition.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    #set cec partner flag on template choices field
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    # if cec_part_selection is None:
        # cec_part_selection = cec_part_init_selection
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id, 'college':m.college_name_id} for m in campus_filter_qs]

    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
    charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')
    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)
    MissionObject = json.loads(charts_missions)

    missionList = []
    for m in MissionObject:
        res = {'id': m['mission_area_id'], 'name': m['mission_area_name'], 'color': m['mission_color'], 'mission_descr': m['mission_descr']}
        missionList.append(res)
    missionList = sorted(missionList, key=lambda i: i['name'])

    defaultyr = AcademicYear.objects.all()
    defaultYrID = defaultyr[defaultyr.count() - 2].id

    return render(request, 'charts/missionchart.html',
                  {'project_filter': project_filter, 'data_definition': data_definition,
                   'campus_filter': campus_filter, 'communityPartners': communityPartners, 'college_filter':college_filter,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection, 'defaultYrID':defaultYrID,
                   'Projects':Projects, 'CommunityPartners':CommunityPartners, 'CampusPartners':CampusPartners, 'missionList':missionList })


@login_required()
def partnershipintensity(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    legislative_choices = []
    legislative_search = ''
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    # legislative_choices.append('All')
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

    y_selection = request.GET.get('y_axis', None)
    y_init_selection = "campus"
    # if y_selection is None:
        # y_selection = y_init_selection
    y_choices = YChoiceForm(initial={'y_choice': y_selection})

    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id, 'college':m.college_name_id} for m in campus_filter_qs]

    community_filter_qs = CommunityPartner.objects.all()
    community_filter = [{'name': m.name, 'id': m.id} for m in community_filter_qs]

    #set cec partner flag on template choices field
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    # if cec_part_selection is None:
    #     cec_part_selection = "All"
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

#########################
    # static_charts_projects = open('home/static/charts_json/projects.json')
    # static_charts_communities = open('home/static/charts_json/community_partners.json')
    # static_charts_campuses = open('home/static/charts_json/campus_partners.json')
    # static_charts_missions = open('home/static/charts_json/mission_subcategories.json')
    # Projects = json.load(static_charts_projects)
    # CommunityPartners = json.load(static_charts_communities)
    # CampusPartners = json.load(static_charts_campuses)
    # MissionObject = json.load(static_charts_missions)
#########################

    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
    charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')
    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)
    MissionObject = json.loads(charts_missions)

    missionList = []
    for m in MissionObject:
        res = {'id': m['mission_area_id'], 'name': m['mission_area_name'], 'color': m['mission_color']}
        missionList.append(res)
    missionList = sorted(missionList, key=lambda i: i['name'])

    defaultyr = AcademicYear.objects.all()
    defaultYrID = defaultyr[defaultyr.count() - 2].id

    return render(request, 'charts/partnershipintensity.html',
                  {'data_definition': data_definition, 'project_filter': project_filter,
                  'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                   'communityPartners': communityPartners, 'campus_filter': campus_filter, 'community_filter':community_filter,
                   'college_filter': college_filter, 'y_choices': y_choices, 'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,
                   'CommunityPartners': CommunityPartners, 'missionList': missionList, 'defaultYrID': defaultYrID,
                   'Projects':Projects, 'CampusPartners':CampusPartners})


# Trend Report Chart
@login_required()
@admin_required()
def trendreport(request):
    data_definition = DataDefinition.objects.all()

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id, 'college':m.college_name_id} for m in campus_filter_qs]

    #set cec partner flag on template choices field
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    # if cec_part_selection is None:
    #     cec_part_selection = cec_part_init_selection
    # print('CEC Partner set in view ' + cec_part_selection)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    yearList = []
    for y in AcademicYear.objects.all():
        res = {'id': y.id, 'name': y.academic_year}
        yearList.append(res)

    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)

    return render(request, 'charts/trendreport.html',
                  { 'missions_filter': missions_filter, 'project_filter': project_filter, 'data_definition': data_definition,
                    'campus_filter': campus_filter, 'college_filter':college_filter, 'communityPartners': communityPartners,
                    'campus_filter': campus_filter, 'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,
                    'yearList':yearList, 'CampusPartners':CampusPartners, 'CommunityPartners': CommunityPartners, 'Projects':Projects})

@login_required()
def EngagementType_Chart(request):
    data_definition = DataDefinition.objects.all()
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    defaultyr = AcademicYear.objects.all()
    defaultYrID = defaultyr[defaultyr.count() - 2].id

    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id, 'college':m.college_name_id} for m in campus_filter_qs]

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    engagements = EngagementType.objects.all()
    engagementList = []
    for e in engagements:
        res = {'id': e.id, 'name': e.name, 'description': e.description}
        engagementList.append(res)
    engagementList = sorted(engagementList, key=lambda i: i['name'])

    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    Projects = json.loads(charts_projects)
    CommunityPartners = json.loads(charts_communities)
    CampusPartners = json.loads(charts_campuses)

    return render(request, 'charts/engagementtypechart2.html',
                 {'missions_filter': missions_filter, 'academicyear_filter': year_filter,'data_definition':data_definition,
                  'campus_filter': campus_filter, 'communityPartners' : communityPartners, 'college_filter': college_filter,
                  'engagementList':engagementList, 'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection, 'defaultYrID':defaultYrID,
                  'Projects':Projects, 'CommunityPartners':CommunityPartners, 'CampusPartners':CampusPartners})


def GEOJSON():
    # if (os.path.isfile('home/static/GEOJSON/Partner.geojson')):  # check if the GEOJSON is already in the DB
    #     with open('home/static/GEOJSON/Partner.geojson') as f:
    #         geojson1 = json.load(f)  # get the GEOJSON
    #     collection = geojson1  # assign it the collection variable to avoid changing the other code
    content_object_partner = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Partner.geojson')
    partner_geojson_load = content_object_partner.get()['Body'].read().decode('utf-8')
    collection = json.loads(partner_geojson_load)
    mission_list = MissionArea.objects.all()
    mission_list = [str(m.mission_name) +':'+str(m.mission_color) for m in mission_list]
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
    geojsondata = GEOJSON()
    Campuspartner = geojsondata[3]
    data = geojsondata[0]
    # Campuspartner = set(Campuspartner[0])
    # Campuspartner = list(Campuspartner)
    json_data = open('home/static/GEOJSON/USCounties_final.geojson')
    county = json.load(json_data)

    return render(request, 'home/Countymap.html',
                  {'countyData': county, 'collection': geojsondata[0],
                   'Missionlist': sorted(geojsondata[1]),
                   'CommTypeList': sorted(geojsondata[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': geojsondata[4]
                   }
                  )



def GEOJSON2():
    # if (os.path.isfile('home/static/GEOJSON/Project.geojson')):  # check if the GEOJSON is already in the DB
    #     with open('home/static/GEOJSON/Project.geojson') as f:
    #         geojson1 = json.load(f)  # get the GEOJSON
    #     collection = geojson1  # assign it the collection variable to avoid changing the other code
    content_object_project = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'geojson/Project.geojson')
    project_geojson_load = content_object_project.get()['Body'].read().decode('utf-8')
    collection = json.loads(project_geojson_load)
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
    map_json_data = GEOJSON2()
    Campuspartner = map_json_data[4]
    Communitypartner = map_json_data[3]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    data = map_json_data[0]
    return render(request, 'home/projectMap.html',
                  {'districtData': district, 'collection': map_json_data[0],
                   'number': len(data['features']),
                   'Missionlist': sorted(map_json_data[2]),
                   'CommTypelist': sorted(map_json_data[5]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'Communitypartner': sorted(Communitypartner),
                   'EngagementType': sorted(map_json_data[1]),
                   'year': sorted(map_json_data[6]),'data_definition':data_definition,
                   'Collegename': (map_json_data[7])
                   }
                  )


def googleDistrictdata(request):
    data_definition = DataDefinition.objects.all()
    map_json_data = GEOJSON()
    Campuspartner = map_json_data[3]
    data = map_json_data[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/legislativeDistrict.html',
                  {'districtData': district, 'collection': map_json_data[0],
                   'Missionlist': sorted(map_json_data[1]),
                   'CommTypeList': sorted(map_json_data[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'number': len(data['features']),
                   'year': sorted(map_json_data[4]),'data_definition':data_definition,
                   'Collegename': map_json_data[6]
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
    map_json_data = GEOJSON()
    Campuspartner = map_json_data[3]
    College = map_json_data[6]
    data = map_json_data[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/communityPartnerType.html',
                  {'collection': data, 'districtData': district,
                   'Missionlist': sorted(map_json_data[1]),
                   'CommTypeList': sorted(map_json_data[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': (Campuspartner),
                   'number': len(data['features']),
                   'year': map_json_data[4],'data_definition':data_definition,
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
                'uid': url_has_allowed_host_and_scheme(force_bytes(new_user.pk)).decode(),
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
        uid = force_str(url_has_allowed_host_and_scheme(uidb64))
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




##### Get the Chart JSONS for network Analysis ##############
def chartjsons():
    # with open('home/static/GEOJSON/ID2.geojson') as f:
    #     geojson = json.load(f)
    #
    # district = geojson["features"]
    # campus_partner=open('home/static/charts_json/campus_partners.json')
    campus_partner_json=json.loads(charts_campuses)
    # campus_partner_json = json.load(campus_partner)#local
    # community_partner = open('home/static/charts_json/community_partners.json')
    community_partner_json = json.loads(charts_communities)
    # community_partner_json = json.load(community_partner)#local
    # mission_subcategories = open('home/static/charts_json/mission_subcategories.json')
    mission_subcategories_json = json.loads(charts_missions)
    # mission_subcategories_json = json.load(mission_subcategories)#local
    # projects =open ('home/static/charts_json/projects.json')
    projects_json = json.loads(charts_projects)
    # projects_json = json.load(projects)#local
    return (campus_partner_json,community_partner_json,mission_subcategories_json,projects_json)



###Network Analysis Chart
@login_required()
def networkanalysis(request):
    data_definition = DataDefinition.objects.all()
    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
    charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')

    campus_partner_json = json.loads(charts_campuses)
    community_partner_json = json.loads(charts_communities)
    mission_subcategories_json = json.loads(charts_missions)
    projects_json = json.loads(charts_projects)

    CollegeNamelist = []
    for e in College.objects.all():
        if (str(e.college_name) not in CollegeNamelist):
            if (str(e.college_name) != "N/A"):
                CollegeNamelist.append({'cname': str(e.college_name), 'id': e.id})
    yrs = []
    acad_years = AcademicYear.objects.all()
    for e in acad_years:
        res={'id':e.id,'year':e.academic_year}
        yrs.append(res)
    acyear = sorted(yrs, key=lambda i: i['year'], reverse=True)

    year_ids=[]
    year_names=[]
    for e in acyear:
        year_ids.append(e['id'])
        year_names.append(e['year'])
    max_yr_id=year_ids[1]
    max_year = year_names[1]
    missionList = []
    for m in MissionArea.objects.all():
        res = {'id': m.id, 'name': m.mission_name, 'color': m.mission_color}
        missionList.append(res)
    missionList = sorted(missionList, key=lambda i: i['name'])


    mission = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.order_by('academic_year'))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    community_filter_qs = CommunityPartner.objects.all()
    community_filter = [{'name': m.name, 'id': m.id} for m in community_filter_qs]

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_init_selection = "All"
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
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


    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id, 'college': m.college_name_id} for m in campus_filter_qs]

    legislative_choices = []
    legislative_search = ''
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'


    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
            legislative_district=legislative_search))





    return render(request, 'charts/network.html',
                  { 'Missionlist': missionList,'data_definition':data_definition,'Collegenames':CollegeNamelist,
                   'campus_partner_json':campus_partner_json,'community_partner_json':community_partner_json,'max_yr_id':max_yr_id,'max_year':max_year,
                   'mission_subcategories_json':mission_subcategories_json,'projects_json':projects_json,
                    'project_filter': project_filter,'campus_filter': campus_filter,'missions': mission,'communityPartners': communityPartners,
                    'college_filter': college_filter,'k12_choices': k12_choices,
                    'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,'cec_part_choices': cec_part_choices,'community_filter':community_filter} )




@login_required()
###Focus Area Analysis Chart
def issueaddress(request):
    data_definition = DataDefinition.objects.all()
    charts_project_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/projects.json')
    charts_projects = charts_project_obj.get()['Body'].read().decode('utf-8')
    charts_community_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/community_partners.json')
    charts_communities = charts_community_obj.get()['Body'].read().decode('utf-8')
    charts_campus_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/campus_partners.json')
    charts_campuses = charts_campus_obj.get()['Body'].read().decode('utf-8')
    charts_mission_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'charts_json/mission_subcategories.json')
    charts_missions = charts_mission_obj.get()['Body'].read().decode('utf-8')

    campus_partner_json = json.loads(charts_campuses)
    community_partner_json = json.loads(charts_communities)
    mission_subcategories_json = json.loads(charts_missions)
    projects_json = json.loads(charts_projects)

    CollegeNamelist=[]
    for e in College.objects.all():
        if(str(e.college_name) not in CollegeNamelist):
            if (str(e.college_name) != "N/A"):
                CollegeNamelist.append({'cname':str(e.college_name), 'id':e.id})
    yrs = []
    acad_years = AcademicYear.objects.all()
    for e in acad_years:
        res={'id':e.id,'year':e.academic_year}
        yrs.append(res)
    # max_yr_id = max(yrs)
    acyear = sorted(yrs, key=lambda i: i['year'], reverse=True)

    year_ids=[]
    year_names=[]
    for e in acyear:
        year_ids.append(e['id'])
        year_names.append(e['year'])
    # print(year_ids[1])
    # print(year_names[1])
    # max_yr = [p.academic_year for p in (AcademicYear.objects.filter(id = (max_yr_id-1)))]
    max_yr_id=year_ids[1]
    min_yr_id=year_ids[2]
    max_year = year_names[1]
    min_year=year_names[2]
    
    MissionObject = json.loads(charts_missions)
    user_role = request.user.is_superuser
    # print("super user ",user_role)

    missionList = []
    for m in MissionObject:
        res = {'id': m['mission_area_id'], 'name': m['mission_area_name'], 'color': m['mission_color'], 'mission_descr': m['mission_descr']}
        missionList.append(res)
    missionList = sorted(missionList, key=lambda i: i['name'],reverse=True)

    # community_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.all())

    mission = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.order_by('academic_year'))
    from_project_filter = FromProjectFilter(request.GET, queryset=Project.objects.order_by('academic_year'))
    to_project_filter = ToProjectFilter(request.GET, queryset=Project.objects.order_by('academic_year'))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # campus_partner_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

    community_filter_qs = CommunityPartner.objects.all()
    community_filter = [{'name': m.name, 'id': m.id} for m in community_filter_qs]

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    cec_part_init_selection = "All"
    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
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


    campus_filter_qs = CampusPartner.objects.all()
    campus_filter = [{'name': m.name, 'id': m.id,'college':m.college_name_id} for m in campus_filter_qs]



    legislative_choices = []
    legislative_search = ''
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    # legislative_choices.append('All')
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





    return render(request, 'charts/focusareaanalaysis.html',
                  { 'Missionlist': missionList,'data_definition':data_definition,'Collegenames':CollegeNamelist,
                   'campus_partner_json':campus_partner_json,'community_partner_json':community_partner_json,'max_yr_id':max_yr_id,'min_yr_id':min_yr_id,
                   'mission_subcategories_json':mission_subcategories_json,'projects_json':projects_json,
                    'to_project_filter': to_project_filter,'from_project_filter': from_project_filter,'project_filter': project_filter,'campus_filter': campus_filter,'missions': mission,'communityPartners': communityPartners,
                    'communityPartners': communityPartners,'college_filter': college_filter,'k12_choices': k12_choices,
                    'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,'cec_part_choices': cec_part_choices,'community_filter':community_filter,'max_year':max_year,'min_year':min_year,"user_role":user_role} )

def removeExistingProjSub(request):
    cursor = connection.cursor()
    updateProjSub = "update projects_project set other_sub_category = null"
    cursor.execute(updateProjSub)
    connection.commit()
    deleteProjSubMap  = "delete from projects_projectsubcategory"
    cursor.execute(deleteProjSubMap)
    connection.commit()
    cursor.close()
    return render(request, 'home/thanks.html',
                  {'thank': thanks})


def read_project_content():
    projects = []
    FILENAME = "Subcategories_Projects_Prod.xls"
    wb = xlrd.open_workbook(FILENAME) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
    total_proj_count = 0
    #for i in range(1,2): 
    for i in range(sheet.nrows): 
      project = {}
      project['name'] = sheet.cell_value(i, 0)
      project['mission'] = sheet.cell_value(i, 1)
      project['subcat'] = sheet.cell_value(i, 2)
      project['comm'] = sheet.cell_value(i, 3)
      project['campus'] = sheet.cell_value(i, 4)
      project['eng'] = sheet.cell_value(i, 5)
      project['strt_acd_yr'] = sheet.cell_value(i, 6)
      project['strt_sem'] = sheet.cell_value(i, 7)
      project['no_uno_students'] = sheet.cell_value(i, 12)
      project['no_uno_students_hrs'] = sheet.cell_value(i, 13)
      project['no_k12_students'] = sheet.cell_value(i, 15)
      project['no_k12_students_hrs'] = sheet.cell_value(i, 16)
      project['act_type'] = sheet.cell_value(i, 18)

      if str(project['name']) == 'Projects' and str(project['mission']) == 'Mission Areas':
        print('skip the header')
      else:
        total_proj_count = total_proj_count + 1
        projects.append(project)      

    return projects


def uploadProjectSub(request,pk):

    projects =  read_project_content()
    index = int(pk)

    for i in projects:     # iterate the adding operation for records present in csv files      
        comm_list = []
        camp_list = []
        comm = i['comm']
        camp = i['campus']

        if comm.split('  ') is not None:
           for x in comm.split('  '):
              if x != '':
                comm_list.append(x)
        else:
          comm_list.append(comm)

        if camp.split('  ') is not None:
           for x in camp.split('  '):
              if x != '':
                camp_list.append(x)
        else:
          camp_list.append(camp)

        i['comm_list'] = comm_list
        i['camp_list'] = camp_list
        #print('project--',i)               
    proj_count = 0
    proj_notfound  = 0
    proj_nosubCat = 0
    total_project_count = 0
    cursor = connection.cursor()

    startIndex = 0
    endIndex = 0
    if index is not None:
        startIndex = index
        if (index < len(projects)) and (len(projects) - index) > index:
                endIndex = startIndex + 100            
        else:
            endIndex = len(projects)        

    for i in range(startIndex,endIndex):
        x = projects[i]
        total_project_count = total_project_count + 1
        #print('project--',x) 
        mission_name = x['mission']
        unoStds = int(x['no_uno_students'])
        unostdHrs = int(x['no_uno_students_hrs'])
        unoK12std = int(x['no_k12_students'])
        unok12Hrs = int(x['no_k12_students_hrs'])
        act_type = x['act_type']
        mission_name = str(mission_name).split(':')[1]
        #print('after split mission_name --',mission_name)
        proj_name = x['name']
        proj_name = str(proj_name).replace("'","''")

        subcat_name = x['subcat']
        subcat_name = str(subcat_name).replace("'","''")
        acd_yr = x['strt_acd_yr']
        engName = x['eng']
        start_sem = x['strt_sem']
        if start_sem is not None and start_sem != '':
            start_sem = start_sem.upper()

        comm_list = x['comm_list']
        comm_name_list = '('

        camp_list = x['camp_list']
        camp_name_list = '('

        if comm_list is not None:
            name_count = 0
            if len(comm_list) > 0:
                for c in comm_list:
                    commName = str(c).replace("'","''")
                    comm_name_list = comm_name_list + str('\'') + str(commName) + str('\'')
                    if name_count < len(comm_list) - 1:
                        comm_name_list = comm_name_list + str(",")
                        name_count = name_count + 1
      
        comm_name_list = comm_name_list + ')'

        if camp_list is not None:
            name_count = 0
            if len(camp_list) > 0:
                for c in camp_list:
                    campName = str(c).replace("'","''")
                    camp_name_list = camp_name_list + str('\'') + str(campName) + str('\'')
                    if name_count < len(camp_list) - 1:
                        camp_name_list = camp_name_list + str(",")
                        name_count = name_count + 1
          
        camp_name_list = camp_name_list + ')'

        projectId = 0
        subCatId = 0
        subMissnId = 0
        othersubCat = []

        if subcat_name is not None and subcat_name != '' and subcat_name != 'None':
                
            select_proj="select distinct p.id, p.other_sub_category \
            from projects_project p , \
            projects_projectmission pm, \
            projects_projectcampuspartner pcam, \
            projects_projectcommunitypartner pcomm \
            where p.id = pm.project_name_id and pm.mission_type = 'Primary' \
            and pm.mission_id = (select id from home_missionarea m where mission_name = '"+str(mission_name).strip()+"') \
            and p.id = pcam.project_name_id and \
            pcam.campus_partner_id in (select id from partners_campuspartner where name in "+camp_name_list+") \
            and p.id = pcomm.project_name_id and \
            pcomm.community_partner_id in (select id from partners_communitypartner where name in "+comm_name_list+") \
            and p.academic_year_id = (select id from projects_academicyear where academic_year = '"+str(acd_yr)+"') and \
            p.engagement_type_id = (select id from projects_engagementtype where name ='"+str(engName)+"') \
            and p.project_name like '"+str(proj_name).strip()+"%' and upper(p.semester) = '"+str(start_sem)+"' \
            and p.total_uno_students =" +str(unoStds)+ " and p.total_uno_hours ="+str(unostdHrs)+" \
            and p.total_k12_students = "+str(unoK12std)+"  and p.total_k12_hours = "+str(unok12Hrs)+"" 
           
            cursor.execute(select_proj)#,[mission_name,camp_name_list,comm_name_list,acd_yr,engName,proj_name])
            proj_result = cursor.fetchall()
            if proj_result is not None and len(proj_result) >0:

                for obj in proj_result:
                  projectId = obj[0]
                  othersubCat = obj[1]

                  if projectId !=0:
                        select_subcat = "select id from projects_subcategory where upper(sub_category) ='"+str(subcat_name).upper()+"'"
                        #print('select_subcat---',select_subcat)
                        cursor.execute(select_subcat)
                        for obj in cursor.fetchall():
                            #print('subCatId --',obj[0])
                            subCatId = obj[0]

                        if subCatId !=0:
                            select_subcat_msn = "select secondary_mission_area_id from projects_missionsubcategory where sub_category_id ="+str(subCatId)+""
                            #print('select_subcat_msn---',select_subcat_msn)
                            cursor.execute(select_subcat_msn)
                            for obj in cursor.fetchall():
                                subMissnId = obj[0]
                        else:
                            select_other_subcat = "select id from projects_subcategory where upper(sub_category) ='OTHER'"
                            #print('select_other_subcat---',select_other_subcat)
                            cursor.execute(select_other_subcat)
                            for obj in cursor.fetchall():
                                subCatId = obj[0]


                        if subCatId != 0:
                            proj_subcatExist = "select id from projects_projectsubcategory \
                            where sub_category_id ="+str(subCatId)+" and project_name_id ="+str(projectId)
                            cursor.execute(proj_subcatExist)
                            result = cursor.fetchall()
                            if len(result) >0:
                                print('mapping already exists')
                            else: 
                                currdate =timezone.now()
                                projObj = Project.objects.get(id=projectId)
                                subCatObj = SubCategory.objects.get(id=subCatId)
                                projSubCat = ProjectSubCategory(project_name=projObj,sub_category=subCatObj,created_date=currdate,updated_date=currdate)                           
                                projSubCat.save()                    
                  
                        if subMissnId !=0:
                            proj_missionExist = "select id from projects_projectmission \
                            where mission_type = 'Other' and mission_id ="+str(subMissnId)+" and project_name_id ="+str(projectId)
                            cursor.execute(proj_missionExist)
                            missionresult = cursor.fetchall()
                            if len(missionresult) >0:
                                print('mission mapping already exists')
                            else:
                                projObj = Project.objects.get(id=projectId)
                                MissonObj = MissionArea.objects.get(id=subMissnId)
                                projMissionObj = ProjectMission(project_name=projObj,mission_type='Other',mission=MissonObj)
                                projMissionObj.save()
                        else:
                            if othersubCat is None or othersubCat == '':
                                othersubCat= []

                            if subcat_name is not None and subcat_name != '':
                                othersubCat.append(subcat_name)                        
                                update_proj_other_sub_desc = "update projects_project \
                                set other_sub_category = %s where id = %s"
                                #print('tuple(othersubCat)--',othersubCat)
                                #print('update_proj_other_sub_desc --',update_proj_other_sub_desc)
                                cursor.execute(update_proj_other_sub_desc,(othersubCat,projectId))
                                connection.commit()

                        proj_count = proj_count +1
                        print(str(proj_name) + " has been updated with "+str(subcat_name))
                  else:
                        print(str(proj_name) + " not found in database ")
                        proj_notfound = proj_notfound + 1
            else:
                proj_notfound = proj_notfound + 1

        else:
            print(str(proj_name) + " has no sub sub_category "+str(subcat_name))
            proj_nosubCat = proj_nosubCat + 1

    print('startIndex',str(startIndex))
    print('endIndex',str(endIndex))
    print(str(proj_count) + " has been updated")
    print(str(proj_notfound) + " not found in database")
    print(str(proj_nosubCat) + " has not sub sub_category")
    print("read", str(total_project_count) + " projects ")
    
    cursor.close()
    return render(request, 'home/thanks.html',
                  {'thank': thanks})

