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
# import pandas as pd
import os

# Google Maps API Key
gmaps = googlemaps.Client(key='AIzaSyBoBkkxBnB7x_GKESVPDLguK0VxSTSxHiI')
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


    return render(request, 'home/ContactUs.html', {
    'form': form_class,
})

def thanks(request):
    return render(request, 'home/thanks.html',
                  {'thank': thanks})


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

            campuspartneruser = CampusPartnerUser(campus_partner=campus_partner_user_form.cleaned_data['campus_partner'], user=new_user)
            campuspartneruser.save()

            return render(request, 'home/register_done.html', )
    else:
        user_form = CampususerForm()
        campus_partner_user_form = CampusPartnerUserForm()

    return render(request,
                  'home/registration/campus_partner_user_register.html',
                  {'user_form': user_form, 'campus_partner_user_form': campus_partner_user_form, 'data':data})


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
            communitypartneruser = CommunityPartnerUser(community_partner=community_partner_user_form.cleaned_data['community_partner'], user=new_user)
            communitypartneruser.save()
            return render(request, 'home/communityuser_register_done.html', )
    return render(request,
                  'home/registration/community_partner_user_register.html',
                  {'user_form': user_form, 'community_partner_user_form': community_partner_user_form
                   ,'commPartner':commPartner})

# uploading the projects data via csv file

@login_required()
@admin_required()
def upload_project(request):
    if request.method == 'GET':
        download_projects_url = '/media/projects_sample.csv'
        return render(request, 'import/uploadProject.html',
                      {'download_projects_url': download_projects_url})
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        campus_query = CampusPartner.objects.all()
        campus_names = [campus.name for campus in campus_query]
        community_query = CommunityPartner.objects.all()
        community_names = [community.name for community in community_query]
        for row in reader:
            data_dict = dict(OrderedDict(row))
            # county_data = countyGEO()
            # district = districtGEO()
    #         if data_dict['address_line1'] != '':
    #             full_address = data_dict['address_line1'] + ' ' + data_dict['city'] + ' ' + data_dict['state']
    #             geocode_result = gmaps.geocode(full_address)
    #             data_dict['latitude'] = round(geocode_result[0]['geometry']['location']['lat'], 7)
    #             data_dict['longitude'] = round(geocode_result[0]['geometry']['location']['lng'], 7)
    #         coord = Point([data_dict['longitude'], data_dict['latitude']])
    #         data_dict['legislative_district'] = 0  # a placeholder value
    #         for i in range(len(district)):  # iterate through a list of district polygons
    #             property = district[i]
    #             polygon = shape(property['geometry'])  # get the polygons
    #             if polygon.contains(coord):  # check if a partner is in a polygon
    #                 data_dict['legislative_district'] = property["id"]  # assign the district number to a partner
    #
    #         data_dict['median_household_income'] = 0  # placeholder value of the income
    #         # get the county name and household income
    #         for m in range(len(county_data)):  # iterate through the County Geojson
    #             properties2 = county_data[m]
    #             polygon = shape(properties2['geometry'])  # get the polygon
    #             if polygon.contains(coord):  # check if the partner in question belongs to a polygon
    #                 data_dict['county'] = properties2['properties']['NAME']
    #                 data_dict['median_household_income'] = properties2['properties']['Income']
            form = UploadProjectForm(data_dict)
            print(form)
            campus = data_dict['campus_partner'] in campus_names
            community = data_dict['community_partner'] in community_names
            if campus and community and form.is_valid():
                form.save()
                form_campus = UploadProjectCampusForm(data_dict)
                form_community = UploadProjectCommunityForm(data_dict)
                form_mission = UploadProjectMissionForm(data_dict)
                # print(form_campus)
                # print(form_community)
                # print(form_mission)
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
    #             # if (str(community_mission[0]) not in Missionlist):  #check if the mission area is already recorded
    #             #     Missionlist.append(str(community_mission[0]))   #add
    #             feature['properties']['CommunityType'] = str(commPartner.community_type)
    #             if campus_id_list:
    #                 feature['properties']['Campus Partner'] = list(set(campus_id_list))
    #                 # CampusPartnerlist.append(list(set(campus_id_list)))
    #             # if (str(commPartner.community_type) not in CommTypelist): #check if the community type is already recorded
    #             #     CommTypelist.append(str(commPartner.community_type)) #add
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
    decoded = csv_file.read().decode('ISO 8859-1' ).splitlines()
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
                    print(form)
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
    mission_dict = {}
    mission_list = []
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    for m in missions:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]
        legislative_filter = legislativeFilter(request.GET, queryset=Project.objects.all())
        legislative_Filter_ids = [project.id for project in legislative_filter.qs]
        proj1_ids = list(set(campus_filtered_ids).intersection(project_filtered_ids))
        project_ids = list(set(proj1_ids).intersection(legislative_Filter_ids))
        mission_dict['mission_name'] = m.mission_name
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=project_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=project_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_list_new = []
        for i in communityPartners.qs:
            if i.id in community_list:
                community_list_new.append(i.id)
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id).\
            filter(community_partner_id__in=community_list_new).count()
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
    return render(request, 'reports/14ProjectPartnerInfo.html', {'project_filter': project_filter,
                  'communityPartners': communityPartners, 'mission_list': mission_list, 'campus_filter': campus_filter})


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
    project_count_data = list()
    partner_count_data = list()
    for m in missions:
        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        proj_ids = [p.id for p in project_filter.qs]
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_project_ids = [p.id for p in campus_filter.qs]
        mission_area1.append(m.mission_name)
        year_filter = AcademicYearFilter(request.GET, queryset=Project.objects.all())
        year_ids = [year.id for year in year_filter.qs]
        project_count = ProjectMission.objects.filter(mission=m.id).filter(project_name_id__in=proj_ids).\
            filter(project_name_id__in=year_ids).filter(project_name_id__in=campus_project_ids).count()
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct()
        community_list = [c.community_partner_id for c in p_community]
        community_count = CommunityPartnerMission.objects.filter(mission_area_id=m.id). \
            filter(community_partner_id__in=community_list).count()
        project_count_data.append(project_count)
        partner_count_data.append(community_count)
    Max_count = max(list(set(partner_count_data) | set(project_count_data)),default=1)
    print(Max_count)

    project_count_series = {
            'name': 'Project Count',
            'data': project_count_data,
            'color': 'turquoise'}
    partner_count_series = {
            'name': 'Community Partner Count',
            'data': partner_count_data,
            'color': 'teal'}
    print(partner_count_series)
    print(project_count_series)
    chart = {
            'chart': {'type': 'bar'},
            'title': {'text': '   '},
            'xAxis': {'title': {'text': 'Mission Areas'}, 'categories': mission_area1},
            'yAxis': {'title': {'text': 'Projects/Community Partners '}, 'min': 0, 'max': Max_count+5},
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

    dump = json.dumps(chart)
    return render(request, 'charts/missionchart.html',{'chart': dump , 'project_filter' : project_filter,
    'year_filter' :year_filter, 'campus_filter':campus_filter })


def EngagementType_Chart(request):
    project_engagement_count = []
    engagment_community_counts = []
    engagment_campus_counts = []
    project_engagement_series = []
    engagament_names = []
    missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    academicyear_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())
    engagement_types = EngagementType.objects.all()
    for et in engagement_types:
        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_project_ids = [p.id for p in campus_filter.qs]
        engagament_names.append(et.name)
        missions_filter = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
        project_mission_ids = [p.project_name_id for p in missions_filter.qs]
        academicyear_filter = AcademicYearFilter(request.GET, queryset=AcademicYear.objects.all())
        project_academicyear_ids = [p.id for p in academicyear_filter.qs]
        proj_id_sem = Project.objects.filter(academic_year_id__in=project_academicyear_ids).\
            filter(id__in=project_mission_ids)
        filtered_project_list = [p.id for p in proj_id_sem]
        project_count = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list).\
            filter(id__in=campus_project_ids).count()
        project_engagement_count.append(project_count)
        projects = Project.objects.filter(engagement_type_id=et.id).filter(id__in=filtered_project_list)
        proj_ids = [p.id for p in projects]
        p_community = ProjectCommunityPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_community_counts.append(p_community)
        p_campus = ProjectCampusPartner.objects.filter(project_name_id__in=proj_ids).distinct().count()
        engagment_campus_counts.append(p_campus)

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
        'xAxis': {'title': {'text': 'Engagement Types'},'categories': engagament_names},
        'yAxis': {'title': {'text': 'Projects/Partners'}, 'min': 0, 'max': Max_count+7},
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
        'series': [project_engagement_series, engagment_community_series, engagment_campus_series]
    }

    dump = json.dumps(chart)
    return render(request, 'charts/engagementtypechart2.html',
                 {'chart': dump, 'missions_filter': missions_filter, 'academicyear_filter': academicyear_filter,
                  'campus_filter': campus_filter})


def GEOJSON():
    commPartners = CommunityPartner.objects.all()  # get all the community partners
    collection = {'type': 'FeatureCollection', 'features': []}  # create the shell of GEOJSON
    if (os.path.isfile('home/static/GEOJSON/Partner.geojson')): #check if the GEOJSON is already in the DB
        print("I am here")
        with open('home/static/GEOJSON/Partner.geojson') as f:
            geojson1 = json.load(f) #get the GEOJSON
        collection = geojson1 #assign it the collection variable to avoid changing the other code
        database_comm = [c.name for c in commPartners]
        if (len(collection["features"]) > len(database_comm)):
            print(collection["features"])
            geo_comm = [c["properties"]["CommunityPartner"] for c in collection["features"]]
            temp3 = [x for x in geo_comm if x not in database_comm]
            index = geo_comm.index(temp3[0])
            print(geo_comm[index])
            collection["features"].remove(collection["features"][index])
            # collection = {'type': 'FeatureCollection', 'features': commpartner}
            jsonstring = pd.io.json.dumps(collection)
            output_filename = 'home/static/GEOJSON/Partner.geojson'  # The file will be saved under static/GEOJSON
            with open(output_filename, 'w') as output_file:
                output_file.write(format(jsonstring))
    # else:
    #     countyData = countyGEO()
    #     district = districtGEO()
    #     #if there is no file, meaning that this is the first initial upload. Create the GEOJSON
    #     print("I am there")
    #
    #     for commPartner in commPartners: #iterate through all community partners
    #         #prepare the shell of the features key inside the GEOJSON
    #         feature = {'type': 'Feature', 'properties': {'CommunityPartner': '', 'Address': '',
    #                                                      'Legislative District Number': '', 'Number of projects': '',
    #                                                      'Income': '', 'County': '', 'Mission Area': '',
    #                                                      'CommunityType': '', 'Campus Partner': '',
    #                                                      'Academic Year': '', 'Website': ''},
    #                    'geometry': {'type': 'Point', 'coordinates': []}
    #                    }
    #         if (commPartner.address_line1 != "N/A"): #check if a community partner's address is there
    #             fulladdress = commPartner.address_line1 + ' ' + commPartner.city + ' ' + commPartner.state
    #             geocode_result = gmaps.geocode(fulladdress) #get the coordinates
    #             commPartner.latitude = geocode_result[0]['geometry']['location']['lat']
    #             commPartner.longitude = geocode_result[0]['geometry']['location']['lng']
    #             coord = Point([commPartner.longitude, commPartner.latitude])
    #
    #              #this is to prepare a variable to check which district a partner belongs to
    #
    #             commPartner.legislative_district = 0          #a placeholder value
    #
    #             for i in range(len(district)):          #iterate through a list of district polygons
    #                 property = district[i]
    #                 polygon = shape(property['geometry'])  #get the polygons
    #                 if polygon.contains(coord):         #check if a partner is in a polygon
    #                     commPartner.legislative_district = property["id"] #assign the district number to a partner
    #             commPartner.median_household_income = 0          #placeholder value of the income
    #
    #             ### get the county name and household income ###
    #             for m in range(len(countyData)): #iterate through the County Geojson
    #                 properties2 = countyData[m]
    #                 polygon = shape(properties2['geometry']) #get the polygon
    #                 if polygon.contains(coord):             #check if the partner in question belongs to a polygon
    #                     commPartner.county = properties2['properties']['NAME']
    #                     commPartner.median_household_income = properties2['properties']['Income']
    #
    #             ### set the value for the feature variable  ######
    #             feature['geometry']['coordinates'] = [commPartner.longitude, commPartner.latitude]
    #             feature['properties']['CommunityPartner'] = commPartner.name
    #             feature['properties']['Address'] = fulladdress
    #             feature['properties']['Website'] = commPartner.website_url
    #             feature['properties']['Legislative District Number'] = commPartner.legislative_district
    #             feature['properties']['Income'] = commPartner.median_household_income
    #             feature['properties']['County'] = commPartner.county
    #             feature['properties']['Number of projects'] = ProjectCommunityPartner.objects.filter(community_partner_id=commPartner.id).count()
    #             ### get the mission area######
    #             community_qs = CommunityPartnerMission.objects.filter(community_partner__id=commPartner.id)
    #             community_mission = [c.mission_area for c in community_qs]
    #             project_ids = ProjectCommunityPartner.objects.filter(community_partner_id=commPartner.id)
    #             project_id_list = [p.project_name_id for p in project_ids]
    #             campus_ids = ProjectCampusPartner.objects.filter(project_name_id__in=project_id_list)
    #             campus_id_list = [str(c.campus_partner) for c in campus_ids]
    #             projectlist = Project.objects.filter(id__in=project_id_list)
    #             year_list = [str(c.academic_year) for c in projectlist]
    #             try:
    #                 feature['properties']['Mission Area'] = str(community_mission[0])
    #                 # if (str(community_mission[0]) not in Missionlist):  #check if the mission area is already recorded
    #                 #     Missionlist.append(str(community_mission[0]))   #add
    #                 feature['properties']['CommunityType'] = str(commPartner.community_type)
    #                 if campus_id_list:
    #                     feature['properties']['Campus Partner'] = list(set(campus_id_list))
    #
    #                     # CampusPartnerlist.append(list(set(campus_id_list)))
    #                 # if (str(commPartner.community_type) not in CommTypelist): #check if the community type is already recorded
    #                 #     CommTypelist.append(str(commPartner.community_type)) #add
    #                 if year_list:
    #                     feature['properties']['Academic Year'] = list(set(year_list))
    #             except:
    #                 print("No mission")
    #             collection['features'].append(feature)  #create the geojson
    #         jsonstring = pd.io.json.dumps(collection)
    #
    #         output_filename = 'home/static/GEOJSON/Partner.geojson'  #The name and location have to match with the one on line 625 in this current function
    #         with open(output_filename, 'w') as output_file:
    #             output_file.write(format(jsonstring)) #write the file to the location
    mission_list = MissionArea.objects.all()
    mission_list = [m.mission_name for m in mission_list]
    CommTypelist = CommunityType.objects.all()
    CommTypelist = [m.community_type for m in CommTypelist]
    CampusPartnerlist = CampusPartner.objects.all()
    CampusPartnerlist = [m.name for m in CampusPartnerlist]
    projectlist = Project.objects.all()
    yearlist = [str(c.academic_year) for c in projectlist]
    yearlist = list(set(yearlist))
    return (collection, sorted(mission_list), sorted(CommTypelist), sorted(CampusPartnerlist), sorted(yearlist))

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
                   'CommTypeList': sorted(GEOJSON()[2]), #pass the array of unique mission areas and community types
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
                   'CommTypeList': sorted(GEOJSON()[2]), #pass the array of unique mission areas and community types
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
                   'CommTypeList': sorted(GEOJSON()[2]), #pass the array of unique mission areas and community types
                   'Campuspartner': sorted(Campuspartner),
                   'number': len(data['features']),
                   'year': GEOJSON()[4]
                   }
                  )

def GEOJSON2():


    if (os.path.isfile('home/static/GEOJSON/Project.geojson')): #check if the GEOJSON is already in the DB
        with open('home/static/GEOJSON/Project.geojson') as f:
            geojson1 = json.load(f) #get the GEOJSON
        collection = geojson1 #assign it the collection variable to avoid changing the other code
    # projects = Project.objects.filter() #get all the projects
    #
    # collection = {'type': 'FeatureCollection', 'features': []} #create the shell of GEOJSON
    # Missionlist = [] ## a placeholder array of unique mission areas
    # Engagementlist = []
    # Academicyearlist = []
    # for project in projects: #iterate through all projects
    #     #prepare the shell of the features key inside the GEOJSON
    #     feature = {'type': 'Feature', 'properties': {'Project Name': '', 'Address': '','Engagement Type': '',
    #                                                   'Legislative District Number': '',
    #                                                  'Income': '', 'County': '', 'Mission Area': '',
    #                                                  },
    #                'geometry': {'type': 'Point', 'coordinates': []}}
    #     if (project.address_line1 != "N/A"): #check if a project address is there
    #
    #         fulladdress = project.address_line1 + ' ' + project.city + ' ' + project.state
    #         ### set the value for the feature variable  ######
    #         feature['geometry']['coordinates'] = [project.longitude, project.latitude]
    #         feature['properties']['Project Name'] = project.project_name
    #         feature['properties']['Address'] = fulladdress
    #         feature['properties']['Activity Type'] = str(project.activity_type)
    #         feature['properties']['Academic year'] = str(project.academic_year)
    #         feature['properties']['Legislative District Number'] = project.legislative_district
    #         feature['properties']['Income'] = project.median_household_income
    #         feature['properties']['County'] = project.county
    #         ### get the mission area######
    #         project_qs = ProjectMission.objects.filter(project_name__id=project.id)
    #         project_mission = [p.mission for p in project_qs]
    #
    #         try:
    #             feature['properties']['Engagement Type'] = str(project.engagement_type)
    #             if (str(project.engagement_type) not in Engagementlist):
    #                 Engagementlist.append(str(project.engagement_type))
    #
    #             feature['properties']['Academic year'] = str(project.academic_year)
    #             if (str(project.academic_year) not in Academicyearlist):
    #                 Academicyearlist.append(str(project.academic_year))
    #
    #             feature['properties']['Mission Area'] = str(project_mission[0])
    #             if (str(project_mission[0]) not in Missionlist):  #check if the mission area is already recorded
    #                 Missionlist.append(str(project_mission[0]))   #add
    #
    #         except:
    #             print("No mission")
    #         collection['features'].append(feature)  #create the geojson
    # #jsonstring = pd.io.json.dumps(collection)
    return (collection)

 ###Project map export to javascript

def projectdata(request):

   json_data = open('home/static/GEOJSON/ID2.geojson')
   district = json.load(json_data)
   data = GEOJSON2()
   return render(request, 'home/projectmap.html',
                      {'districtData': district, 'collection': GEOJSON2(),
                       'number': len(data["features"])
                       }
                      )