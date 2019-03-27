import json
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from home.decorators import campuspartner_required, admin_required
from django.contrib.auth import authenticate, login, logout
import csv
from collections import OrderedDict
import sys
sys.setrecursionlimit(1500)
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
import googlemaps
from shapely.geometry import shape, Point
import pandas as pd
import os

# Google Maps API Key
gmaps = googlemaps.Client(key='AIzaSyBH5afRK4l9rr_HOR_oGJ5Dsiw2ldUzLv0')


#


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
    return render(request, 'home/homepage.html',
                  {'home': home})


def MapHome(request):
    return render(request, 'home/Map_Home.html',
                  {'MapHome': MapHome})


def Definitions(request):
    data_definition = DataDefinition.objects.values('id', 'title', 'description', 'group_id')
    for group_id in data_definition:
        group = group_id['group_id']
        data_definition_group = DataDefinitionGroup.objects.filter(pk=group)
    return render(request, 'home/DataDefinitions.html',
                  {'data_definition': data_definition},
                  {'data_definition_group': data_definition_group})


# def Contactus(request):
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
            topic = request.POST.get('topic', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('home/contact_template.txt')
        context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'topic': topic,
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

    return render(request, 'home/ContactUs.html', {
        'form': form_class,
    })


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
            new_user.is_campuspartner = True
            new_user.save()

            campuspartneruser = CampusPartnerUser(
                campus_partner=campus_partner_user_form.cleaned_data['campus_partner'], user=new_user)
            campuspartneruser.save()

            return render(request, 'home/register_done.html', )
    else:
        user_form = CampususerForm()
        campus_partner_user_form = CampusPartnerUserForm()

    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form, 'data': data})


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
            # county_data = countyGEO()
            # district = districtGEO()
            # if data_dict['address_line1'] != '':
            #     full_address = data_dict['address_line1'] + ' ' + data_dict['city'] + ' ' + data_dict['state']
            #     geocode_result = gmaps.geocode(full_address)
            #     data_dict['latitude'] = round(geocode_result[0]['geometry']['location']['lat'], 7)
            #     data_dict['longitude'] = round(geocode_result[0]['geometry']['location']['lng'], 7)
            # coord = Point([data_dict['longitude'], data_dict['latitude']])
            # data_dict['legislative_district'] = 0  # a placeholder value
            # for i in range(len(district)):  # iterate through a list of district polygons
            #     property = district[i]
            #     polygon = shape(property['geometry'])  # get the polygons
            #     if polygon.contains(coord):  # check if a partner is in a polygon
            #         data_dict['legislative_district'] = property["id"]  # assign the district number to a partner
            #
            # data_dict['median_household_income'] = 0  # placeholder value of the income
            # # get the county name and household income
            # for m in range(len(county_data)):  # iterate through the County Geojson
            #     properties2 = county_data[m]
            #     polygon = shape(properties2['geometry'])  # get the polygon
            #     if polygon.contains(coord):  # check if the partner in question belongs to a polygon
            #         data_dict['county'] = properties2['properties']['NAME']
            #         data_dict['median_household_income'] = properties2['properties']['Income']
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
    # countyData = countyGEO()
    # district = districtGEO()
    # commPartners = CommunityPartner.objects.all()  # get all the community partners
    # collection = {'type': 'FeatureCollection', 'features': []}  # create the shell of GEOJSON
    # for commPartner in commPartners:  # iterate through all community partners
    #     # prepare the shell of the features key inside the GEOJSON
    #     feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '',
    #                                                  'Legislative District Number': '', 'Number of projects': '',
    #                                                  'Income': '', 'County': '', 'Mission Area': '',
    #                                                  'CommunityType': '', 'Campus Partner': '',
    #                                                  'Academic Year': '', 'Website': ''},
    #                'geometry': {'type': 'Point', 'coordinates': []}}
    #     if (commPartner.address_line1 != "N/A"):  # check if a community partner's address is there
    #         fulladdress = commPartner.address_line1 + ' ' + commPartner.city + ' ' + commPartner.state
    #         geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
    #         commPartner.latitude = geocode_result[0]['geometry']['location']['lat']
    #         commPartner.longitude = geocode_result[0]['geometry']['location']['lng']
    #         coord = Point([commPartner.longitude, commPartner.latitude])
    #
    #         # this is to prepare a variable to check which district a partner belongs to
    #
    #         commPartner.legislative_district = 0  # a placeholder value
    #
    #         for i in range(len(district)):  # iterate through a list of district polygons
    #             property = district[i]
    #             polygon = shape(property['geometry'])  # get the polygons
    #             if polygon.contains(coord):  # check if a partner is in a polygon
    #                 commPartner.legislative_district = property["id"]  # assign the district number to a partner
    #         commPartner.median_household_income = 0  # placeholder value of the income
    #
    #         ### get the county name and household income ###
    #         for m in range(len(countyData)):  # iterate through the County Geojson
    #             properties2 = countyData[m]
    #             polygon = shape(properties2['geometry'])  # get the polygon
    #             if polygon.contains(coord):  # check if the partner in question belongs to a polygon
    #                 commPartner.county = properties2['properties']['NAME']
    #                 commPartner.median_household_income = properties2['properties']['Income']
    #
    #         ### set the value for the feature variable  ######
    #         feature['geometry']['coordinates'] = [commPartner.longitude, commPartner.latitude]
    #         feature['properties']['CommunityPartner'] = commPartner.name
    #         feature['properties']['Address'] = fulladdress
    #         feature['properties']['Website'] = commPartner.website_url
    #         feature['properties']['Legislative District Number'] = commPartner.legislative_district
    #         feature['properties']['Income'] = commPartner.median_household_income
    #         feature['properties']['County'] = commPartner.county
    #         feature['properties']['Number of projects'] = ProjectCommunityPartner.objects.filter(
    #             community_partner_id=commPartner.id).count()
    #         ### get the mission area######
    #         community_qs = CommunityPartnerMission.objects.filter(community_partner__id=commPartner.id)
    #         community_mission = [c.mission_area for c in community_qs]
    #         project_ids = ProjectCommunityPartner.objects.filter(community_partner_id=commPartner.id)
    #         project_id_list = [p.project_name_id for p in project_ids]
    #         campus_ids = ProjectCampusPartner.objects.filter(project_name_id__in=project_id_list)
    #         campus_id_list = [str(c.campus_partner) for c in campus_ids]
    #         projectlist = Project.objects.filter(id__in=project_id_list)
    #         year_list = [str(c.academic_year) for c in projectlist]
    #         try:
    #             feature['properties']['Mission Area'] = str(community_mission[0])
    #             if (str(community_mission[0]) not in Missionlist):  #check if the mission area is already recorded
    #                 Missionlist.append(str(community_mission[0]))   #add
    #             feature['properties']['CommunityType'] = str(commPartner.community_type)
    #             if campus_id_list:
    #                 feature['properties']['Campus Partner'] = list(set(campus_id_list))
    #                 CampusPartnerlist.append(list(set(campus_id_list)))
    #             if (str(commPartner.community_type) not in CommTypelist): #check if the community type is already recorded
    #                 CommTypelist.append(str(commPartner.community_type)) #add
    #             if year_list:
    #                 feature['properties']['Academic Year'] = list(set(year_list))
    #         except:
    #             print("No mission")
    #         collection['features'].append(feature)  # create the geojson
    #     jsonstring = pd.io.json.dumps(collection)
    #
    #     output_filename = 'home/static/GEOJSON/Partner.geojson'  # The name and location have to match with the one on line 625 in this current function
    #     with open(output_filename, 'w') as output_file:
    #         output_file.write(format(jsonstring))  # write the file to the location
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
        # county_data = countyGEO()
        # district = districtGEO()
        # if data_dict['address_line1'] != '':
        #     full_address = data_dict['address_line1'] + ' ' + data_dict['city'] + ' ' + data_dict['state']
        #     geocode_result = gmaps.geocode(full_address)
        #     data_dict['latitude'] = round(geocode_result[0]['geometry']['location']['lat'], 7)
        #     data_dict['longitude'] = round(geocode_result[0]['geometry']['location']['lng'], 7)
        # coord = Point([data_dict['longitude'], data_dict['latitude']])
        # # this is to prepare a variable to check which district a partner belongs to
        # # coord = Point(commPartner.longitude, commPartner.latitude)
        # data_dict['legislative_district'] = 0  # a placeholder value
        # for i in range(len(district)):  # iterate through a list of district polygons
        #     property = district[i]
        #     polygon = shape(property['geometry'])  # get the polygons
        #     if polygon.contains(coord):  # check if a partner is in a polygon
        #         data_dict['legislative_district'] = property["id"]  # assign the district number to a partner
        #
        # data_dict['median_household_income'] = 0  # placeholder value of the income
        # # get the county name and household income
        # for m in range(len(county_data)):  # iterate through the County Geojson
        #     properties2 = county_data[m]
        #     polygon = shape(properties2['geometry'])  # get the polygon
        #     if polygon.contains(coord):  # check if the partner in question belongs to a polygon
        #         data_dict['county'] = properties2['properties']['NAME']
        #         data_dict['median_household_income'] = properties2['properties']['Income']
        # community_count = CommunityPartner.objects.filter(name=data_dict['name']).count()
        # if community_count == 0:

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


# (14) Mission Summary Report: filter by Semester, EngagementType


def project_partner_info(request):
    missions = MissionArea.objects.all()
    data_definition = DataDefinition.objects.all()
    mission_dict = {}
    mission_list = []
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    for m in missions:

        college_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        college_filtered_ids = [campus.id for campus in college_filter.qs]
        campus_project_filter= ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=college_filtered_ids))
        campus_project_filter_ids = [project.project_name_id for project in campus_project_filter.qs]

        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]

        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        community_filtered_ids = [community.id for community in communityPartners.qs]

        comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(community_partner_id__in=community_filtered_ids))
        comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]

        proj1_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
        proj2_ids = list(set(campus_project_filter_ids).intersection(proj1_ids))
        project_ids = list(set(proj2_ids).intersection(comm_filtered_ids))

        mission_dict['mission_name'] = m.mission_name
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids).filter(mission_type='Primary').count()

        proj_comm = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).filter(community_partner_id__in=community_filtered_ids).distinct()
        proj_comm_ids = [community.community_partner_id for community in proj_comm]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=proj_comm_ids).count()

        p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids).filter(mission_type='Primary')

        a = request.GET.get('engagement_type', None)
        b = request.GET.get('academic_year', None)
        c = request.GET.get('campus_partner', None)
        d = request.GET.get('college_name', None)
        if a is None or a == "All" or a == '':
            if b is None or b == "All" or b == '':
                if c is None or c == "All" or c == '':
                    if d is None or d == "All" or d == '':
                        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).filter(mission_type='Primary').filter(community_partner_id__in=community_filtered_ids).count()

        e = request.GET.get('community_type', None)
        f = request.GET.get('weitz_cec_part', None)
        if f is None or f == "All" or f == '':
            if e is None or e == "All" or e == '':
                p_mission = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj2_ids).filter(mission_type='Primary')
                project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj2_ids).filter(mission_type='Primary').count()

        mission_dict['project_count'] = project_count
        mission_dict['community_count'] = community_count
        total_uno_students = 0
        total_uno_hours = 0

        for pm in p_mission:
            uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        mission_dict['total_uno_hours'] = total_uno_hours
        mission_dict['total_uno_students'] = total_uno_students
        mission_list.append(mission_dict.copy())
    return render(request, 'reports/ProjectPartnerInfo.html',
                  {'project_filter': project_filter, 'data_definition': data_definition,
                   'communityPartners': communityPartners, 'mission_list': mission_list,
                   'campus_filter': campus_filter, 'college_filter':college_filter})


# (15) Engagement Summary Report: filter by AcademicYear, MissionArea


def engagement_info(request):

    engagements = EngagementType.objects.all()
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    data_definition = DataDefinition.objects.all()
    engagement_Dict = {}
    engagement_List = []
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    for e in engagements:

        campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
        campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
        campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]

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

        # gets the prpject ids for one engagement type
        proj_comm = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)

        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_comm_1 = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_comm).distinct()

        # gets all the community partner ids in a array. These are not distinct
        proj_comm_ids = [community.community_partner_id for community in proj_comm_1]

        # sets the non distinct array to a distinct set of community partner ids
        unique_comm_ids = set(proj_comm_ids)

        # counts within the set of unique community partner ids
        unique_comm_ids_count = len(unique_comm_ids)

        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_comm).distinct()

        # gets all the campus partner ids in a array. These are not distinct
        proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]

        # sets the non distinct array to a distinct set of campus partner ids
        unique_camp_ids = set(proj_camp_ids)

        # counts within the set of unique campus partner ids
        unique_camp_ids_count = len(unique_camp_ids)

        engagement_Dict['engagement_name'] = e.name
        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list).count()

        a = request.GET.get('weitz_cec_part', None)
        b = request.GET.get('community_type', None)
        if a is None or b == "All" or a == '':
            if b is None or b == "All" or b == '':
                project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_ids1).count()

        engagement_Dict['project_count'] = project_count
        engagement_Dict['community_count'] = unique_comm_ids_count
        engagement_Dict['campus_count'] = unique_camp_ids_count
        total_uno_students = 0
        total_uno_hours = 0

        projects = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)
        for p in projects:
            uno_students = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=p.id).aggregate(Sum('total_uno_hours'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
        engagement_Dict['total_uno_hours'] = total_uno_hours
        engagement_Dict['total_uno_students'] = total_uno_students
        engagement_List.append(engagement_Dict.copy())
    return render(request, 'reports/EngagementTypeReport.html',
                  {'college_filter': campus_partner_filter, 'missions_filter': missions_filter, 'year_filter': year_filter, 'engagement_List': engagement_List,
                   'data_definition':data_definition, 'communityPartners' : communityPartners ,'campus_filter': campus_filter})


# (15) Engagement Summary Report: filter by AcademicYear, MissionArea


def unique_count(request):
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    project_year_ids = [p.id for p in year_filter.qs]
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    mission_ids = [m.mission_id for m in missions_filter.qs]
    project_missions = [p.project_name_id for p in missions_filter.qs]
    unique_project_ids = list(set(campus_filtered_ids).intersection(project_year_ids))
    total_unique_project = list(set(unique_project_ids).intersection(project_missions))
    unique_project = len(total_unique_project)

    # community partner count
    community_mission_filter = CommunityPartnerMission.objects.filter(mission_area_id__in=mission_ids)
    community_mission_ids = [c.community_partner_id for c in community_mission_filter]
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

    dump = json.dumps(chart)
    return render(request, 'charts/missionchart.html',
                  {'chart': dump, 'project_filter': project_filter, 'data_definition': data_definition,
                    'campus_filter': campus_filter, 'communityPartners': communityPartners, 'college_filter':college_filter})


def EngagementType_Chart(request):
    engagements = EngagementType.objects.all()
    year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    data_definition = DataDefinition.objects.all()
    engagement_Dict = {}
    engagement_List = []
    project_engagement_count = []
    engagment_community_counts = []
    engagment_campus_counts = []
    project_engagement_series = []
    engagament_names = []
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    for e in engagements:

        campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
        campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
            campus_partner_id__in=campus_partner_filtered_ids))
        campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]

        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
        project_mission_ids = [p.project_name_id for p in missions_filter.qs]

        year_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_year_ids = [project.id for project in year_filter.qs]

        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        community_filtered_ids = [community.id for community in communityPartners.qs]
        comm_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
            community_partner_id__in=community_filtered_ids))
        comm_filtered_ids = [project.project_name_id for project in comm_filter.qs]

        filtered_project_ids = list(set(project_mission_ids).intersection(project_year_ids))
        filtered_project_ids2 = list(set(campus_project_filtered_ids).intersection(filtered_project_ids))
        filtered_project_ids1 = list(set(campus_filtered_ids).intersection(filtered_project_ids2))
        filtered_project_list = list(set(comm_filtered_ids).intersection(filtered_project_ids1))

        # gets the prpject ids for one engagement type
        proj_comm = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list)

        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_comm_1 = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_comm).distinct()

        # gets all the community partner ids in a array. These are not distinct
        proj_comm_ids = [community.community_partner_id for community in proj_comm_1]

        # sets the non distinct array to a distinct set of community partner ids
        unique_comm_ids = set(proj_comm_ids)

        # counts within the set of unique community partner ids
        unique_comm_ids_count = len(unique_comm_ids)

        # gets the distinct ids from projectcommunity partner table for all the above projects
        proj_camp = ProjectCampusPartner.objects.filter(project_name_id__in=proj_comm).distinct()

        # gets all the campus partner ids in a array. These are not distinct
        proj_camp_ids = [campus.campus_partner_id for campus in proj_camp]

        # sets the non distinct array to a distinct set of campus partner ids
        unique_camp_ids = set(proj_camp_ids)

        # counts within the set of unique campus partner ids
        unique_camp_ids_count = len(unique_camp_ids)

        project_count = Project.objects.filter(engagement_type_id=e.id).filter(id__in=filtered_project_list).count()

        a = request.GET.get('weitz_cec_part', None)
        b = request.GET.get('community_type', None)
        if a is None or b == "All" or a == '':
            if b is None or b == "All" or b == '':
                project_count = Project.objects.filter(engagement_type_id=e.id).filter(
                    id__in=filtered_project_ids1).count()

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

    dump = json.dumps(chart)
    return render(request, 'charts/engagementtypechart2.html',
                 {'chart': dump, 'missions_filter': missions_filter, 'academicyear_filter': year_filter,'data_definition':data_definition,
                  'campus_filter': campus_filter, 'communityPartners' : communityPartners, 'college_filter': campus_partner_filter})


def GEOJSON():
    CollegeNamelist = []
    # commPartners = CommunityPartner.objects.all()  # get all the community partners
    # collection = {'type': 'FeatureCollection', 'features': []}  # create the shell of GEOJSON
    if (os.path.isfile('home/static/GEOJSON/Partner.geojson')):  # check if the GEOJSON is already in the DB
        with open('home/static/GEOJSON/Partner.geojson') as f:
            geojson1 = json.load(f)  # get the GEOJSON
        collection = geojson1  # assign it the collection variable to avoid changing the other code
        # database_comm = [c.name for c in commPartners]
        # if (len(collection["features"]) > len(database_comm)):
        #     geo_comm = [c["properties"]["CommunityPartner"] for c in collection["features"]]
        #     temp3 = [x for x in geo_comm if x not in database_comm]
        #     index = geo_comm.index(temp3[0])
        #     collection["features"].remove(collection["features"][index])
        #     # collection = {'type': 'FeatureCollection', 'features': commpartner}
        #     jsonstring = pd.io.json.dumps(collection)
        #     output_filename = 'home/static/GEOJSON/Partner.geojson'  # The file will be saved under static/GEOJSON
        #     with open(output_filename, 'w') as output_file:
        #         output_file.write(format(jsonstring))
    else:
        countyData = countyGEO()
        district = districtGEO()
        # if there is no file, meaning that this is the first initial upload. Create the GEOJSON

        for commPartner in CommunityPartner.objects.all():


        # for commPartner in commPartners:  # iterate through all community partners
        #     # prepare the shell of the features key inside the GEOJSON
        #     feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '',
        #                                                  'Legislative District Number': '', 'Number of projects': '',
        #                                                  'Income': '', 'City': '', 'County': '','Mission Type': '',
        #                                                  'Mission Area': '',
        #                                                  'CommunityType': '','College Name': '', 'Campus Partner': '',
        #                                                  'Academic Year': '', 'Website': '', 'Projects': ''},
        #                'geometry': {'type': 'Point', 'coordinates': []}
        #                }
        #     if (commPartner.address_line1 != "N/A"):  # check if a community partner's address is there
        #         fulladdress = commPartner.address_line1 + ' ' + commPartner.city + ' ' + commPartner.state
        #         geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
        #         commPartner.latitude = geocode_result[0]['geometry']['location']['lat']
        #         commPartner.longitude = geocode_result[0]['geometry']['location']['lng']
        #         coord = Point([commPartner.longitude, commPartner.latitude])
        #
        #         # this is to prepare a variable to check which district a partner belongs to
        #
        #         commPartner.legislative_district = 0  # a placeholder value
        #
        #         for i in range(len(district)):  # iterate through a list of district polygons
        #             property = district[i]
        #             polygon = shape(property['geometry'])  # get the polygons
        #             if polygon.contains(coord):  # check if a partner is in a polygon
        #                 commPartner.legislative_district = property["id"]  # assign the district number to a partner
        #         commPartner.median_household_income = 0  # placeholder value of the income
        #
        #         ### get the county name and household income ###
        #         for m in range(len(countyData)):  # iterate through the County Geojson
        #             properties2 = countyData[m]
        #             polygon = shape(properties2['geometry'])  # get the polygon
        #             if polygon.contains(coord):  # check if the partner in question belongs to a polygon
        #                 commPartner.county = properties2['properties']['NAME']
        #                 commPartner.median_household_income = properties2['properties']['Income']
        #
        #         ### set the value for the feature variable  ######
        #         feature['geometry']['coordinates'] = [commPartner.longitude, commPartner.latitude]
        #         feature['properties']['CommunityPartner'] = commPartner.name
        #         feature['properties']['Address'] = fulladdress
        #         feature['properties']['Website'] = commPartner.website_url
        #         feature['properties']['Legislative District Number'] = commPartner.legislative_district
        #         feature['properties']['Income'] = commPartner.median_household_income
        #         feature['properties']['County'] = commPartner.county
        #         feature['properties']['City'] = commPartner.city
        #         feature['properties']['Number of projects'] = ProjectCommunityPartner.objects.filter(
        #             community_partner_id=commPartner.id).count()
        #         feature['properties']['Projects'] = ProjectCommunityPartner.objects.filter(community_partner_id=commPartner.id)
                ### get the mission area######
                community_qs = CommunityPartnerMission.objects.filter(community_partner__id=commPartner.id)
                community_mission = [c.mission_area for c in community_qs]
                project_ids = ProjectCommunityPartner.objects.filter(community_partner_id=commPartner.id)
                project_id_list = [p.project_name_id for p in project_ids]
                campus_ids = ProjectCampusPartner.objects.filter(project_name_id__in=project_id_list)
                campus_id_list = [str(c.campus_partner) for c in campus_ids]
                projectlist = Project.objects.filter(id__in=project_id_list)
                year_list = [str(c.academic_year) for c in projectlist]

                # try:
                    # feature['properties']['Mission Area'] = str(community_mission[0])
                    # if (str(community_mission[0]) not in Missionlist):  #check if the mission area is already recorded
                    #     Missionlist.append(str(community_mission[0]))   #add
                    # feature['properties']['CommunityType'] = str(commPartner.community_type)
                    # if campus_id_list:
                    #     feature['properties']['Campus Partner'] = list(set(campus_id_list))

                        # CampusPartnerlist.append(list(set(campus_id_list)))
                    # if (str(commPartner.community_type) not in CommTypelist): #check if the community type is already recorded
                    #     CommTypelist.append(str(commPartner.community_type)) #add
                    # if year_list:
                    #     feature['properties']['Academic Year'] = list(set(year_list))
                # except:
                #     print("No mission")
                # collection['features'].append(feature)  # create the geojson
            # jsonstring = pd.io.json.dumps(collection)

            # output_filename = 'home/static/GEOJSON/Partner.geojson'  # The name and location have to match with the one on line 625 in this current function
            # with open(output_filename, 'w') as output_file:
            #     output_file.write(format(jsonstring))  # write the file to the location
    mission_list = MissionArea.objects.all()
    mission_list = [m.mission_name for m in mission_list]
    CommTypelist = CommunityType.objects.all()
    CommTypelist = [m.community_type for m in CommTypelist]
    CampusPartner_qs = CampusPartner.objects.all()
    CampusPartnerlist = [m.name for m in CampusPartner_qs]
    collegeName_list = College.objects.all()
    collegeName_list = collegeName_list.exclude(college_name__exact="N/A")
    collegeNamelist = [m.college_name for m in collegeName_list]
    projectlist = Project.objects.all()
    # yearlist = [str(c.academic_year) for c in projectlist]
    # strearlist = AcademicYear.objects.all()
    yearlist=[]
    for year in AcademicYear.objects.all():
        yearlist.append(year.academic_year)
    commPartnerlist = CommunityPartner.objects.all()
    commPartnerlist = [m.name for m in commPartnerlist]
    return (collection, sorted(mission_list), sorted(CommTypelist), sorted(CampusPartnerlist), sorted(yearlist),
            sorted(commPartnerlist), sorted(collegeNamelist))


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


def partnerdata(request):
    Campuspartner = GEOJSON()[3]
    data = GEOJSON()[0]

    return render(request, 'home/homepage.html',
                  {'collection': data,
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4]
                   }
                  )


def districtdata(request):
    Campuspartner = GEOJSON()[3]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/Districtmap.html',
                  {'districtData': district, 'collection': GEOJSON()[0],
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4],
                   }
                  )


def GEOJSON2():
    if (os.path.isfile('home/static/GEOJSON/Project.geojson')):  # check if the GEOJSON is already in the DB
        with open('home/static/GEOJSON/Project.geojson') as f:
            geojson1 = json.load(f)  # get the GEOJSON
        collection = geojson1  # assign it the collection variable to avoid changing the other code
    # projects = Project.objects.filter()  # get all the projects

    # collection = {'type': 'FeatureCollection', 'features': []}  # create the shell of GEOJSON
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
                CollegeNamelist.append(str(e.college_name))


    for year in AcademicYear.objects.all():
        Academicyearlist.append(year.academic_year)

    for mission in MissionArea.objects.all():
        Missionlist.append(mission.mission_name)

    for engagement in EngagementType.objects.all():
        Engagementlist.append(engagement.name)

    for communitypart in CommunityPartner.objects.all():
        CommunityPartnerlist.append(communitypart.name)

    for campuspart in CampusPartner.objects.all():
        CampusPartnerlist.append(campuspart.name)

    # for project in Project.objects.all():

    # for project in projects:  # iterate through all projects
    #     # prepare the shell of the features key inside the GEOJSON
    #     feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Engagement Type': '', 'Activity Type': '',
    #                                              'Description': '', 'Academic Year': '',
    #                                              'Legislative District Number':'','College Name': '',
    #                                              'Campus Partner': '', 'Community Partner':'', 'Mission Area':'','Community Partner Type':'',
    #                                              'Address Line1':'', 'City':'', 'State':'', 'Zip':''},
    #                'geometry': {'type': 'Point', 'coordinates': []}}
    #     ### get the community partner type######
    #     # communityType_qs = CommunityPartner.objects.filter(name__exact=communitypartner[0])
    #     # communityType_qs = CommunityType.objects.all()
    #     # community_type = [p.community_type for p in communityType_qs]
    #
    #
    #     # get the college name
    #     # college_qs = CampusPartner.objects.filter(name__exact=campuspartner[0])
    #     college_qs = College.objects.all()
    #     college_name = [p.college_name for p in college_qs]
    #
    #     if (project.address_line1 != "N/A"):  # check if a project address is there
    #         fulladdress = project.address_line1 + ' ' + project.city + ' ' + project.state
    #         geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
    #         project.latitude = geocode_result[0]['geometry']['location']['lat']
    #         project.longitude = geocode_result[0]['geometry']['location']['lng']
    #         coord = Point([project.longitude, project.latitude])
    #         ### set the value for the feature variable  ######
    #         feature['geometry']['coordinates'] = [project.longitude, project.latitude]
    #         feature['properties']['Project Name'] = project.project_name
    #         feature['properties']['Address'] = fulladdress
    #         feature['properties']['Activity Type'] = str(project.activity_type)
    #         feature['properties']['Academic Year'] = str(project.academic_year)
    #         feature['properties']['Legislative District Number'] = project.legislative_district
    #         feature['properties']['City'] = project.city
            ### get the mission area######
            # project_qs = ProjectMission.objects.filter(project_name__id=project.id)
            # project_mission = [p.mission for p in project_qs]



            # ### get the community partner######
            # community_qs = ProjectCommunityPartner.objects.filter(project_name__id=project.id)
            # communitypartner = [p.community_partner for p in community_qs]
            #
            # ### get the campus partner######
            # campus_qs = ProjectCampusPartner.objects.filter(project_name__id=project.id)
            # campuspartner = [p.campus_partner for p in campus_qs]

            # print(project_mission)



            # try:
                # feature['properties']['College Name'] = str(college_name[0])
                # if (str(college_name[0]) not in CollegeNamelist):
                #     CollegeNamelist.append(str(college_name[0]))

                # feature['properties']['Community Partner'] = str(communitypartner[0])
                # if (str(communitypartner[0]) not in CommunityPartnerlist):
                #     CommunityPartnerlist.append(str(communitypartner[0]))
                #
                # # feature['properties']['Campus Partner'] = str(campuspartner[0])
                # if (str(campuspartner[0]) not in CampusPartnerlist):
                #     CampusPartnerlist.append(str(campuspartner[0]))

                # feature['properties']['Community Partner Type'] = str(community_type[0])
                # if (str(community_type[0]) not in CommunityPartnerTypelist):
                #     CommunityPartnerTypelist.append(str(community_type[0]))

                # feature['properties']['Engagement Type'] = str(project.engagement_type)
                # if (str(project.engagement_type) not in Engagementlist):
                #     Engagementlist.append(str(project.engagement_type))


                # feature['properties']['Mission Area'] = str(project_mission[0])
                # if (str(project_mission[0]) not in Missionlist):  # check if the mission area is already recorded
                #     Missionlist.append(str(project_mission[0]))  # add

            # except:
            #     print("No mission")
            # collection['features'].append(feature)  # create the geojson
    # jsonstring = pd.io.json.dumps(collection)
    return (collection, sorted(Engagementlist),sorted(Missionlist),sorted(CommunityPartnerlist),
            sorted(CampusPartnerlist), sorted(CommunityPartnerTypelist),sorted(Academicyearlist), sorted(CollegeNamelist))


###Project map export to javascript

def projectdata(request):
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    data = GEOJSON2()
    return render(request, 'home/projectmap.html',
                  {'districtData': district, 'collection': GEOJSON2(),
                   'number': len(data['features'])
                   }
                  )


# google maps implementaiton
def googleprojectdata(request):
    Campuspartner = GEOJSON2()[4]
    Communitypartner = GEOJSON2()[3]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    data = GEOJSON2()[0]
    return render(request, 'home/googleprojectmap.html',
                  {'districtData': district, 'collection': GEOJSON2()[0],
                   'number': len(data['features']),
                   'Missionlist': sorted(GEOJSON2()[2]),
                   'CommTypelist': sorted(GEOJSON2()[5]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'Communitypartner': sorted(Communitypartner),
                   'EngagementType': sorted(GEOJSON2()[1]),
                   'year': sorted(GEOJSON2()[6]),
                   'Collegename': sorted(GEOJSON2()[7])
                   }
                  )


def googleDistrictdata(request):
    Campuspartner = GEOJSON()[3]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/googleDistrictmap.html',
                  {'districtData': district, 'collection': GEOJSON()[0],
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': sorted(GEOJSON()[4]),
                   'Collegename': GEOJSON()[6]
                   }
                  )


def googlepartnerdata(request):
    Campuspartner = GEOJSON()[3]
    College = GEOJSON()[6]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/googlehomepage.html',
                  {'collection': data, 'districtData':district,
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4],
                   'College': sorted(College)
                   }
                  )


def googlemapdata(request):
    Campuspartner = GEOJSON()[3]
    College = GEOJSON()[6]
    data = GEOJSON()[0]
    json_data = open('home/static/GEOJSON/ID2.geojson')
    district = json.load(json_data)
    return render(request, 'home/googlemap.html',
                  {'collection': data, 'districtData': district,
                   'Missionlist': sorted(GEOJSON()[1]),
                   'CommTypeList': sorted(GEOJSON()[2]),  # pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4],
                   'College': sorted(College)
                   }
                  )