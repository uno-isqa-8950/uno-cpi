from decimal import *
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from numpy import shape

import home
from django.views.decorators.csrf import csrf_exempt
from home.decorators import communitypartner_required, campuspartner_required, admin_required
from home.views import gmaps
from partners.views import district, countyData
from projects.models import *
from home.models import *
from home.filters import *
from partners.models import *
from university.models import Course
from .forms import ProjectCommunityPartnerForm, CourseForm, ProjectFormAdd, AddSubCategoryForm
from django.contrib.auth.decorators import login_required
from .models import Project,ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, Status ,EngagementType, ActivityType, ProjectSubCategory
from .forms import ProjectForm, ProjectMissionForm, ScndProjectMissionFormset, K12ChoiceForm, CecPartChoiceForm, OommCecPartChoiceForm
from django.shortcuts import render, redirect, get_object_or_404 , get_list_or_404
from django.utils import timezone
from  .forms import ProjectMissionFormset,AddProjectCommunityPartnerForm, AddProjectCampusPartnerForm,ProjectForm2, ProjectMissionEditFormset
from django.forms import inlineformset_factory, modelformset_factory
from .filters import SearchProjectFilter
import googlemaps
from shapely.geometry import shape, Point
import pandas as pd
import json
from django.db.models import Sum
import datetime
from django.conf import settings
from googlemaps import Client
# The imports below are for running sql queries for AllProjects Page
from django.db import connection
from UnoCPI import sqlfiles
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

sql=sqlfiles
gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)


@login_required()
@communitypartner_required()
def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)

#    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome,'usertype':usertype})


@login_required()
def myProjects(request):
    projects_list=[]
    data_definition=DataDefinition.objects.all()
    camp_part_user = CampusPartnerUser.objects.filter(user_id = request.user.id)
    camp_part_id = camp_part_user.values_list('campus_partner_id', flat=True)
    proj_camp = ProjectCampusPartner.objects.filter(campus_partner__in=camp_part_id)
    project_ids = [project.project_name_id for project in proj_camp]
    cursor = connection.cursor()
    cursor.execute(sql.my_projects, [project_ids])
    for obj in cursor.fetchall():
        projects_list.append(
            {"name": obj[0].split("(")[0], "projmisn": obj[1], "comm_part": obj[2], "camp_part": obj[3],
             "engagementType": obj[4], "academic_year": obj[5],
             "semester": obj[6], "status": obj[7], "startDate": obj[8], "endDate": obj[9], "outcomes": obj[10],
             "total_uno_students": obj[11],
             "total_uno_hours": obj[12], "total_uno_faculty": obj[13], "total_k12_students": obj[14],
             "total_k12_hours": obj[15],
             "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18],
             "project_type": obj[20], "pk":obj[19]
                , "end_semester": obj[21], "end_academic_year": obj[22], "sub_category": obj[23],
             "campus_lead_staff": obj[24],
             "mission_image": obj[25], "other_activity_type": obj[26], "other_sub_category":obj[27]})

    return render(request, 'projects/myProjects.html', {'project': projects_list, 'data_definition':data_definition})

@login_required()
def communitypartnerproject(request):
    projects_list = []
    data_definition = DataDefinition.objects.all()
    # Get the campus partner id's related to the user
    comm_part_user = CommunityPartnerUser.objects.filter(user_id=request.user.id)
    comm_part_id = comm_part_user.values_list('community_partner_id', flat=True)
    proj_comm = ProjectCommunityPartner.objects.filter(community_partner__in=comm_part_id)
    project_ids = [project.project_name_id for project in proj_comm]
    cursor = connection.cursor()
    cursor.execute(sql.my_projects, [project_ids])
    for obj in cursor.fetchall():
        projects_list.append(
            {"name": obj[0].split("(")[0], "projmisn": obj[1], "comm_part": obj[2], "camp_part": obj[3],
             "engagementType": obj[4], "academic_year": obj[5],
             "semester": obj[6], "status": obj[7], "startDate": obj[8], "endDate": obj[9], "outcomes": obj[10],
             "total_uno_students": obj[11],
             "total_uno_hours": obj[12], "total_uno_faculty": obj[13], "total_k12_students": obj[14],
             "total_k12_hours": obj[15],
             "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18]})
    return render(request, 'projects/community_partner_projects.html', {'project': projects_list,'data_definition':data_definition})

#Old Code for My Projects Page

# @login_required()
# def myProjects(request):
#     projects_list=[]
#     camp_part_names=[]
#     data_definition=DataDefinition.objects.all()
#     # Get the campus partner id's related to the user
#     camp_part_user = CampusPartnerUser.objects.filter(user_id = request.user.id)
#     for c in camp_part_user:
#         p = c.campus_partner_id
#         # get all the project names base on the campus partner id
#         proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id = p))
#         for f in proj_camp:
#             k=list(Project.objects.filter(id = f.project_name_id))
#             for x in k:
#              projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
#              cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
#              proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
#              for proj_camp_par in proj_camp_par:
#                 camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
#
#                 camp_part_names.append(camp_part)
#              list_camp_part_names = camp_part_names
#              camp_part_names = []
#
#              data = {'pk': x.pk, 'name': x.project_name.split(":")[0], 'engagementType': x.engagement_type,
#                 'activityType': x.activity_type, 'academic_year': x.academic_year,
#                 'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,'description':x.description,
#                 'startDate': x.start_date,
#                 'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
#                 'total_uno_hours': x.total_uno_hours,
#                 'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
#                 'total_uno_faculty': x.total_uno_faculty,
#                 'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
#                 'total_economic_impact': x.total_economic_impact,'projmisn': projmisn, 'cp': cp, 'camp_part':list_camp_part_names
#                  }
#
#              projects_list.append(data)
#     return render(request, 'projects/myProjects.html', {'project': projects_list, 'data_definition':data_definition})


def ajax_load_project(request):
    project_name = request.GET.get('name', None)
    data = {
        'is_taken': Project.objects.filter(project_name__iexact=project_name).exists()
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def saveProjectAndRegister(request):
    projectId = request.GET.get('projectId')
    name = request.GET.get('name')
    description = request.GET.get('description')
    engagement_type = request.GET.get('engagement_type')
    activity_type = request.GET.get('activity_type')
    start_semester = request.GET.get('start_semester')
    start_academic_yr = request.GET.get('start_academic_yr')
    end_semester = request.GET.get('end_semester')
    end_academic_yr = request.GET.get('end_academic_yr')
    uno_students = request.GET.get('uno_students')
    uno_students_hrs = request.GET.get('uno_students_hrs')
    k12_students = request.GET.get('k12_students')
    k12_students_hrs = request.GET.get('k12_students_hrs')
    k12_involvment_flag = request.GET.get('k12_involvment_flag')
    comm_list = request.GET.get('selectedCommIds')
    campus_list = request.GET.get('selectedCampusIds')
    project_type = request.GET.get('project_type')
    lead_staff_list = request.GET.get('lead_staff_list')
    k12_flag_value = False
    year_in_project_name = ''

    if k12_involvment_flag == 'on':
        k12_flag_value = True
    if projectId is not None:
        project = Project.objects.get(id=projectId)
    else:
        project = Project(project_name=name)

    project.description=description
    project.semester=start_semester
    project.end_semester=end_semester
    project.total_uno_students=uno_students
    project.total_uno_hours=uno_students_hrs
    project.k12_flag=k12_flag_value
    project.total_k12_students=k12_students
    project.total_k12_hours=k12_students_hrs
    project.project_type=project_type

    if start_academic_yr != '' and start_academic_yr is not None:
        project.academic_year = AcademicYear.objects.get(id=start_academic_yr)
        year_in_project_naame = project.academic_year

    if end_academic_yr != '' and end_academic_yr is not None:
        project.end_academic_year = AcademicYear.objects.get(id=end_academic_yr)

    if engagement_type != '' and engagement_type is not None:
        project.engagement_type = EngagementType.objects.get(id=engagement_type)

    if activity_type != '' and activity_type is not None:
        project.activity_type = ActivityType.objects.get(id=activity_type)

    if lead_staff_list != '' and lead_staff_list is not None:
        lead_name_list = []
        if lead_staff_list.find(",") != -1:
            leadName_list =lead_staff_list.split(",")
            for leadName in leadName_list:
                lead_name_list.append(leadName)
        else:
            lead_name_list.append(lead_staff_list)

        project.campus_lead_staff = lead_name_list

    project.status = Status.objects.get(name='Drafts')

    project.save()
    projectId = project.pk

    project.project_name = name + ": " + str(year_in_project_naame) + " (" + str(projectId) + ")"
    project.save()

    if comm_list != '' or comm_list is not None:
        if comm_list.find(",") != -1:
            comm_Id_list =comm_list.split(",")
        else:
            comm_Id_list = comm_list

        for commId in comm_Id_list:
           comm_obj =  CommunityPartner.objects.get(id=commId)
           proj_obj =  Project.objects.get(id=projectId)
           projComm = ProjectCommunityPartner(project_name=proj_obj,community_partner=comm_obj)
           projComm.save()

    if campus_list != '' or campus_list is not None:
        if campus_list.find(",") != -1:
            camp_id_list =campus_list.split(",")
        else:
            camp_id_list = campus_list

        for campId in camp_id_list:
           camp_obj =  CampusPartner.objects.get(id=campId)
           proj_obj =  Project.objects.get(id=projectId)
           projCamp_obj = ProjectCampusPartner(project_name=proj_obj,campus_partner=camp_obj)
           projCamp_obj.save()

    data = {'save_projectId' : projectId}
    return JsonResponse(data)


def saveFocusArea(request):
    selectedfocusarea = request.GET.get('focusarea')
    projectid = request.GET.get('projectId')
    print('selected focus area ajax--', selectedfocusarea)
    print('selected focus area ajax--', projectid)
    try:
        test = ProjectMission.objects.get(project_name_id=projectid, mission_type='Primary')
    except ProjectMission.DoesNotExist:
        test = None

    if test is not None:
        cursor = connection.cursor()
        cursor.execute(sqlfiles.editproj_updateprimarymission(str(selectedfocusarea), str(projectid)), params=None)
    else:
        cursor = connection.cursor()
        cursor.execute(sqlfiles.editproj_addprimarymission(str(selectedfocusarea), str(projectid)), params=None)


    return projectid

def getEngagemetActivityList(request):
    selectedEngagement = request.GET.get('selectedEngagement')
    print('selectedEngagement--',selectedEngagement)
    activityList = []
    if selectedEngagement is not None:
        engagementObj = EngagementType.objects.get(name=selectedEngagement)
        print("engagemenet Id--",engagementObj.id)
        eng_act_obj = EngagementActivityType.objects.all().filter(EngagementTypeName=engagementObj)
        print('eng_act_obj--',eng_act_obj)
        for act in eng_act_obj:
            print('act obj---',act.ActivityTypeName)
            actObj = ActivityType.objects.get(name=act.ActivityTypeName)
            activityList.append( {"name": actObj.name, "id": actObj.id})

        #otherActivityObj = ActivityType.objects.all().filter(name='Other')
        #print('otherActivityObj--',otherActivityObj)
        #activityList.append( {"name": otherActivityObj.name, "id": otherActivityObj.id})
    print('activityList---',activityList)
    data = {'activityList' : activityList}
    return JsonResponse(data)



@login_required()
def createProject(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    #secondary_mission_details = modelformset_factory(ProjectMission, extra=1, form=ScndProjectMissionFormset)
    sub_category = modelformset_factory(ProjectSubCategory, extra=1, form=AddSubCategoryForm)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition=DataDefinition.objects.all()
    #Populate project name-Parimita
    request.POST.get('id_project_name')
    # if request.method == 'POST' and 'submit' in request.POST:
    if request.method == 'POST':
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        categoryformset = sub_category(request.POST or None, prefix='sub_category')
        formset = mission_details(request.POST or None, prefix='mission')
        #formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        print(project.is_valid())
        print(formset.is_valid() )
        print(formset2.is_valid() )
        print(formset3.is_valid() )
        print(categoryformset.is_valid())
        if project.is_valid() and formset.is_valid() and formset2.is_valid() and formset3.is_valid() and categoryformset.is_valid():


            if request.POST.get('k12_flag'):
                project.k12_flag = True
            else:
                project.k12_flag = False
            #project.created_by = created_by
            proj = project.save()
            proj.project_name = proj.project_name + ": " + str(proj.academic_year) + " (" + str(proj.id) + ")"
            eng = str(proj.engagement_type)
            address = proj.address_line1
            stat = str(proj.status)

            if stat == 'Drafts':

                if (address != ''):
                    if (address != "N/A"):  # check if a community partner's address is there
                        fulladdress = proj.address_line1 + ' ' + proj.city
                        geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
                        proj.latitude = geocode_result[0]['geometry']['location']['lat']
                        proj.longitude = geocode_result[0]['geometry']['location']['lng']
                        #### checking lat and long are incorrect
                        if (proj.latitude == '0') or (proj.longitude == '0'):
                            project = ProjectFormAdd()
                            course = CourseForm()
                            formset = mission_details(queryset=ProjectMission.objects.none())
                            # formset4 = secondary_mission_details(queryset=ProjectMission.objects.none())
                            # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
                            formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
                            return render(request, 'projects/createProject.html',
                                          {'project': project, 'formset': formset, 'formset3': formset3,
                                           'course': course})
                    proj.save()
                    coord = Point([proj.longitude, proj.latitude])
                    for i in range(len(district)):  # iterate through a list of district polygons
                        property = district[i]
                        polygon = shape(property['geometry'])  # get the polygons
                        if polygon.contains(coord):  # check if a partner is in a polygon
                            proj.legislative_district = property["id"]  # assign the district number to a partner
                            proj.save()
                    for m in range(len(countyData)):  # iterate through the County Geojson
                        properties2 = countyData[m]
                        polygon = shape(properties2['geometry'])  # get the polygon
                        if polygon.contains(coord):  # check if the partner in question belongs to a polygon
                            proj.county = properties2['properties']['NAME']
                            proj.median_household_income = properties2['properties']['Income']
                            proj.save()
                    mission_form = formset.save(commit=False)
                    # secondary_mission_form = formset4.save(commit=False)
                    proj_comm_form = formset2.save(commit=False)
                    proj_campus_form = formset3.save(commit=False)
                    sub_cat_form = categoryformset.save(commit=False)
                    for k in proj_comm_form:
                        k.project_name = proj
                        k.save()


                    for cat in sub_cat_form:
                        cat.project_name = proj
                        cat.save()
                        subcategory = str(cat.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(proj.id)), params=None)


                    for form in mission_form:
                        form.project_name = proj

                        form.mission_type = 'Primary'
                        form.save()

                    init = 0
                    t = 0
                    for c in proj_campus_form:
                        c.project_name = proj
                        c.save()
                        proj.save()

                    projects_list = []
                    camp_part_names = []
                    p = 0
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id
                    # get all the project names base on the campus partner id
                    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                    for f in proj_camp:
                        k = list(Project.objects.filter(id=f.project_name_id))
                        for x in k:
                            projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                            sub = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                            cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                            proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                            for proj_camp_par in proj_camp_par:
                                camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []
                            data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes, 'other_activity_type': x.other_activity_type,
                                    'total_economic_impact': x.total_economic_impact,
                                    'campus_lead_staff': x.campus_lead_staff, 'projmisn': projmisn, 'cp': cp,
                                    'sub': sub,
                                    'camp_part': list_camp_part_names,
                                    }
                            projects_list.append(data)

                    return render(request, 'projects/draftadd_done.html', {'project': projects_list})

                if (address == ''):
                    proj.save()
                    mission_form = formset.save(commit=False)
                    # secondary_mission_form = formset4.save(commit=False)
                    sub_cat_form = categoryformset.save(commit=False)
                    proj_comm_form = formset2.save(commit=False)
                    proj_campus_form = formset3.save(commit=False)
                    for k in proj_comm_form:
                        k.project_name = proj
                        k.save()
                    for cat in sub_cat_form:
                        cat.project_name = proj
                        cat.save()
                        subcategory = str(cat.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(proj.id)), params=None)

                    for form in mission_form:
                        form.project_name = proj
                        form.mission_type = 'Primary'
                        form.save()
                    init = 0
                    t = 0
                    for c in proj_campus_form:
                        c.project_name = proj
                        c.save()
                        proj.save()

                    projects_list = []
                    camp_part_names = []
                    p = 0
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id
                    # get all the project names base on the campus partner id
                    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                    for f in proj_camp:
                        k = list(Project.objects.filter(id=f.project_name_id))
                        for x in k:
                            projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                            sub = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                            cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                            proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                            for proj_camp_par in proj_camp_par:
                                camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []
                            data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes, 'other_activity_type': x.other_activity_type,
                                    'total_economic_impact': x.total_economic_impact,
                                    'campus_lead_staff': x.campus_lead_staff, 'projmisn': projmisn, 'cp': cp,
                                    'sub': sub,
                                    'camp_part': list_camp_part_names,
                                    }
                            projects_list.append(data)
                    return render(request, 'projects/draftadd_done.html', {'project': projects_list})
            elif stat == 'Active':
                if(address != ''):
                    if (address != "N/A"):  # check if a community partner's address is there
                        fulladdress = proj.address_line1 + ' ' + proj.city
                        geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
                        proj.latitude = geocode_result[0]['geometry']['location']['lat']
                        proj.longitude = geocode_result[0]['geometry']['location']['lng']
                        #### checking lat and long are incorrect
                        if (proj.latitude == '0') or (proj.longitude == '0'):
                            project = ProjectFormAdd()
                            course = CourseForm()
                            formset = mission_details(queryset=ProjectMission.objects.none())
                            # formset4 = secondary_mission_details(queryset=ProjectMission.objects.none())
                            # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
                            formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
                            return render(request, 'projects/createProject.html',
                                          {'project': project, 'formset': formset, 'formset3': formset3,
                                           'course': course})
                    proj.save()
                    coord = Point([proj.longitude, proj.latitude])
                    for i in range(len(district)):  # iterate through a list of district polygons
                        property = district[i]
                        polygon = shape(property['geometry'])  # get the polygons
                        if polygon.contains(coord):  # check if a partner is in a polygon
                            proj.legislative_district = property["id"]  # assign the district number to a partner
                            proj.save()
                    for m in range(len(countyData)):  # iterate through the County Geojson
                        properties2 = countyData[m]
                        polygon = shape(properties2['geometry'])  # get the polygon
                        if polygon.contains(coord):  # check if the partner in question belongs to a polygon
                            proj.county = properties2['properties']['NAME']
                            proj.median_household_income = properties2['properties']['Income']
                            proj.save()
                    mission_form = formset.save(commit=False)
                    # secondary_mission_form = formset4.save(commit=False)
                    proj_comm_form = formset2.save(commit=False)
                    proj_campus_form = formset3.save(commit=False)
                    sub_cat_form = categoryformset.save(commit=False)
                    for k in proj_comm_form:
                        k.project_name = proj
                        k.save()

                    for cat in sub_cat_form:
                        cat.project_name = proj
                        cat.save()
                        subcategory = str(cat.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(proj.id)), params=None)

                    for form in mission_form:
                        form.project_name = proj

                        form.mission_type = 'Primary'
                        form.save()

                    # for form4 in secondary_mission_form:
                    #     form4.project_name = proj
                    #
                    #     form4.mission_type = 'Other'
                    #     form4.save()

                    # projh = Project.objects.get(pk=project_name_id.pk)
                    init = 0
                    t = 0
                    for c in proj_campus_form:
                        c.project_name = proj
                        c.save()
                        # init = proj.total_uno_hours
                        # t += c.total_hours * c.total_people

                        # proj.total_uno_hours = t
                        proj.save()

                    projects_list = []
                    camp_part_names = []
                    p = 0
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id
                    # get all the project names base on the campus partner id
                    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                    for f in proj_camp:
                        k = list(Project.objects.filter(id=f.project_name_id))
                        for x in k:
                            projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                            sub = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                            cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                            proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                            for proj_camp_par in proj_camp_par:
                                camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []
                            data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes, 'other_activity_type': x.other_activity_type,
                                    'total_economic_impact': x.total_economic_impact,
                                    'campus_lead_staff': x.campus_lead_staff, 'projmisn': projmisn, 'cp': cp,
                                    'sub': sub,
                                    'camp_part': list_camp_part_names,
                                    }
                            projects_list.append(data)
                    return render(request, 'projects/confirmAddProject.html', {'project': projects_list})
                if (address == ''):
                    proj.save()
                    mission_form = formset.save(commit=False)
                    # secondary_mission_form = formset4.save(commit=False)
                    sub_cat_form = categoryformset.save(commit=False)
                    proj_comm_form = formset2.save(commit=False)
                    proj_campus_form = formset3.save(commit=False)
                    for k in proj_comm_form:
                        k.project_name = proj
                        k.save()
                    for cat in sub_cat_form:
                        cat.project_name = proj
                        cat.save()
                        subcategory = str(cat.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(proj.id)), params=None)

                    for form in mission_form:
                        form.project_name = proj
                        form.mission_type = 'Primary'
                        form.save()

                    # """def my_view(request):
                    #     ...
                    #     form = ProjectForm2(request.POST or None)
                    #     if request.method == "POST":
                    #         if form.is_valid():
                    #
                    #             if request.POST["k12_flag"]:
                    #                 # Checkbox was checked"""
                    #                 ...
                    # for form4 in secondary_mission_form:
                    #     form4.project_name = proj
                    #
                    #     form4.mission_type = 'Other'
                    #     form4.save()

                    # projh = Project.objects.get(pk=project_name_id.pk)
                    init = 0
                    t = 0
                    for c in proj_campus_form:
                        c.project_name = proj
                        c.save()
                        # init = proj.total_uno_hours
                        # t += c.total_hours * c.total_people
                        # proj.total_uno_hours = t
                        proj.save()

                    projects_list = []
                    camp_part_names = []
                    p = 0
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id
                    # get all the project names base on the campus partner id
                    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                    for f in proj_camp:
                        k = list(Project.objects.filter(id=f.project_name_id))
                        for x in k:
                            projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                            sub = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                            cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                            proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                            for proj_camp_par in proj_camp_par:
                                camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []
                            data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students,
                                    'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes,
                                    'total_economic_impact': x.total_economic_impact,
                                    'other_activity_type': x.other_activity_type,
                                    'campus_lead_staff': x.campus_lead_staff, 'projmisn': projmisn, 'cp': cp,
                                    'sub': sub,
                                    'camp_part': list_camp_part_names,
                                    }
                            projects_list.append(data)
                    return render(request, 'projects/confirmAddProject.html', {'project': projects_list})
    else:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if month > 7:
            a_year = str(year) + "-" + str(year + 1)[-2:]
        else:
            a_year = str(year - 1) + "-" + str(year)[-2:]

        #  test = AcademicYear.objects.get(academic_year=a_year)
        #  project =ProjectFormAdd(initial={"academic_year":test})
        try:
            test = AcademicYear.objects.get(academic_year=a_year)
        except AcademicYear.DoesNotExist:
            test = None

        if test is not None:
            project = ProjectFormAdd(initial={"academic_year": test})
        else:
            project = ProjectFormAdd()

        course = CourseForm()
        formset = mission_details(queryset=ProjectMission.objects.none(), prefix='mission')
        # formset4 = secondary_mission_details(queryset=ProjectMission.objects.none(), prefix='secondary_mission')
        categoryformset = sub_category(queryset=ProjectSubCategory.objects.none(), prefix='sub_category')
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none(), prefix='community')
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none(), prefix='campus')

    return render(request, 'projects/createProject.html',
                  {'project': project, 'formset': formset, 'formset3': formset3, 'course': course,
                   'data_definition': data_definition,
                   'formset2': formset2, 'categoryformset': categoryformset})


@login_required()
def editProject(request, pk):
    project_mission = ProjectMissionEditFormset()
    proj_comm_part_edit = inlineformset_factory(Project, ProjectCommunityPartner, extra=0, min_num=1, can_delete=True,
                                                form=AddProjectCommunityPartnerForm)
    proj_campus_part_edit = inlineformset_factory(Project, ProjectCampusPartner, extra=0, min_num=1, can_delete=True,
                                                  form=AddProjectCampusPartnerForm)
    sub_category_edit = inlineformset_factory(Project, ProjectSubCategory, extra=0, min_num=1, can_delete=True,
                                              form=AddSubCategoryForm)
    data_definition = DataDefinition.objects.all()
    print('print input to edit')

    if request.method == 'POST':
        # cache.clear()
        proj_edit = Project.objects.filter(id=pk)
        # projectName = request.POST['projectName'].strip()
        # p = request.POST
        # focus_area = request.GET['id_mission_area']
        # print(focus_area)
        for x in proj_edit:
            project = ProjectFormAdd(request.POST or None, instance=x)
            course = CourseForm(request.POST or None, instance=x)
            formset_comm_details = proj_comm_part_edit(request.POST or None, request.FILES, instance=x,
                                                       prefix='community_edit')
            formset_camp_details = proj_campus_part_edit(request.POST or None, request.FILES, instance=x,
                                                         prefix='campus_edit')
            formset_subcatdetails = sub_category_edit(request.POST or None, request.FILES, instance=x,
                                                      prefix='sub_category_edit')

            if project.is_valid() and formset_camp_details.is_valid() and formset_comm_details.is_valid() and formset_subcatdetails.is_valid():
                print('in valid')
                instances = project.save()
                instances.project_name = instances.project_name.split(":")[0] + ": " + str(
                    instances.academic_year) + " (" + pk + ")"
                print (instances.project_name)
                stat = str(instances.status)
                if stat == 'Drafts':
                    instances.save()
                    compar = formset_comm_details.save()
                    campar = formset_camp_details.save()
                    subcat = formset_subcatdetails.save()
                    # focus_areas = focusarea['id_mission']
                    # focus_areas = request.POST.get('id_mission_area',None)
                    # print(focus_areas)

                    # for k in pm:
                    #     k.project_name = instances
                    #     k.save()
                    for p in compar:
                        p.project_name = instances
                        p.save()
                    for l in campar:
                        l.project_name = instances
                        l.save()
                    for sc in subcat:
                        sc.project_name = instances
                        sc.save()
                        subcategory = str(sc.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(pk)), params=None)
                    projects_list = []
                    camp_part_names = []
                    course_list = []
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id

                        # get all the project names base on the campus partner id
                        proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                        for f in proj_camp:
                            k = list(Project.objects.filter(id=f.project_name_id))

                            tot_hours = 0
                            for x in k:

                                # projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                                cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                                proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                                subc = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                                for proj_camp_par in proj_camp_par:
                                    camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                    # tot_hours += proj_camp_par.total_hours * proj_camp_par.total_people
                                    # total_project_hours += proj_camp_par.total_hours
                                    # x.total_uno_hours = tot_hours
                                    # x.total_uno_students += proj_camp_par.total_people
                                    x.save()
                                    camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []

                            data = {'pk': x.pk, 'name': x.project_name.split(":")[0],
                                    'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'other_activity_type': x.other_activity_type,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes,
                                    'total_economic_impact': x.total_economic_impact, 'cp': cp,
                                    'subc': subc,
                                    'camp_part': list_camp_part_names,
                                    }

                            projects_list.append(data)

                    return HttpResponseRedirect("/myDrafts")
                else:
                    instances.save()
                    # pm = formset_missiondetails.save()
                    compar = formset_comm_details.save()
                    campar = formset_camp_details.save()
                    subcat = formset_subcatdetails.save()
                    # for k in pm:
                    #     k.project_name = instances
                    #     k.save()
                    for p in compar:
                        p.project_name = instances
                        p.save()
                    for l in campar:
                        l.project_name = instances
                        l.save()
                    for sc in subcat:
                        sc.project_name = instances
                        sc.save()
                        subcategory = str(sc.sub_category);
                        print(subcategory)
                        cursor = connection.cursor()
                        cursor.execute(sqlfiles.createproj_othermission(subcategory), params=None)
                        rows = cursor.fetchall()
                        print(rows)
                        # print(rows[0])
                        # projmission = projectmission.save()
                        for mission in rows:
                            print(mission[0])
                            id = str(mission[0])
                            # print(id)
                            cursor = connection.cursor()
                            cursor.execute(sqlfiles.createproj_addothermission(id, str(pk)), params=None)
                    projects_list = []
                    camp_part_names = []
                    course_list = []
                    # Get the campus partner id related to the user
                    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
                    for c in camp_part_user:
                        p = c.campus_partner_id

                        # get all the project names base on the campus partner id
                        proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                        for f in proj_camp:
                            k = list(Project.objects.filter(id=f.project_name_id))

                            tot_hours = 0
                            for x in k:

                                # projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                                cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                                proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                                subc = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                                for proj_camp_par in proj_camp_par:
                                    camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                                    # tot_hours += proj_camp_par.total_hours * proj_camp_par.total_people
                                    # total_project_hours += proj_camp_par.total_hours
                                    # x.total_uno_hours = tot_hours
                                    # x.total_uno_students += proj_camp_par.total_people
                                    x.save()
                                    camp_part_names.append(camp_part)
                            list_camp_part_names = camp_part_names
                            camp_part_names = []

                            data = {'pk': x.pk, 'name': x.project_name.split(":")[0],
                                    'engagementType': x.engagement_type,
                                    'activityType': x.activity_type, 'academic_year': x.academic_year,
                                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                                    'description': x.description,
                                    'startDate': x.start_date,
                                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                    'total_uno_hours': x.total_uno_hours,
                                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                    'total_uno_faculty': x.total_uno_faculty,
                                    'total_other_community_members': x.total_other_community_members,
                                    'outcomes': x.outcomes, 'other_activity_type': x.other_activity_type,
                                    'total_economic_impact': x.total_economic_impact,
                                    # 'projmisn': projmisn,
                                    'cp': cp,
                                    'subc': subc,
                                    'camp_part': list_camp_part_names,
                                    }

                            projects_list.append(data)

                    return HttpResponseRedirect("/allProjects")

                # return render(request, 'projects/myProjects.html', {'project': projects_list})

    else:

        proj_edit = Project.objects.get(id=pk)
        print('proj_edit--', proj_edit)
        engagementObj = proj_edit.engagement_type
        print('selected engagemenet type--', engagementObj)
        selectedActivity = proj_edit.activity_type
        print('selected activity type--', selectedActivity)
        eng_act_obj = EngagementActivityType.objects.all().filter(EngagementTypeName=engagementObj)
        print('eng_act_obj--', eng_act_obj)
        activityList = []
        for act in eng_act_obj:
            print('act obj---', act.ActivityTypeName)
            actObj = ActivityType.objects.get(name=act.ActivityTypeName)
            # activityList.append({"name": actObj.name, "id": actObj.id})
            if str(actObj.name)== str(selectedActivity):
                selected = 'selected'
                activityList.append({"name": actObj.name, "id": actObj.id, "selected":selected})
            else:
                activityList.append({"name": actObj.name, "id": actObj.id})
        print (activityList)
            # for x in proj_edit:
        x = proj_edit
        project = ProjectForm2(request.POST or None, instance=x)
        course = CourseForm(instance=x)
        project_mission = ProjectMissionEditFormset()
        project_all_missions = MissionArea.objects.all()
        # mission_areas = []
        # for miss in project_all_missions:
        #     print('missions-----', miss)
        #     mission_areas.append({"name": miss.mission_name, "id": miss.id})
        # print(mission_areas)
        try:
            test = ProjectMission.objects.get(project_name_id=pk,mission_type = 'Primary')
        except ProjectMission.DoesNotExist:
            test = None

        if test is not None:
            proj_mission = ProjectMission.objects.get(project_name_id=pk,mission_type = 'Primary')
        else:
            proj_mission = 'none'

        # print(proj_mission)
        mission_areas = []
        for miss in project_all_missions:
            # print(miss.mission_name)
            if miss.mission_name == str(proj_mission):
                selected = 'selected'
                mission_areas.append({"name": miss.mission_name, "id": miss.id,'selected':selected})
            else:
                mission_areas.append({"name": miss.mission_name, "id": miss.id})

        # print(mission_areas)
        # selectedMisson = proj_mission.mission_id
        proj_comm_part = ProjectCommunityPartner.objects.filter(project_name_id=pk)
        proj_camp_part = ProjectCampusPartner.objects.filter(project_name_id=pk)
        # course_details = course(instance= x)
        # formset_missiondetails = mission_edit_details(instance=x, prefix='mission_edit')
        formset_comm_details = proj_comm_part_edit(instance=x, prefix='community_edit')
        formset_camp_details = proj_campus_part_edit(instance=x, prefix='campus_edit')
        formset_subcat_details = sub_category_edit(instance=x, prefix='sub_category_edit')
        return render(request, 'projects/editProject.html', {'project': project, 'course': course,
                                                             'project_mission':project_mission,
                                                             'mission_areas':mission_areas,
                                                             # 'formset_missiondetails': formset_missiondetails,
                                                             'formset_comm_details': formset_comm_details,
                                                             'formset_camp_details': formset_camp_details,
                                                             'formset_subcat_details': formset_subcat_details,
                                                             'projectId': pk, 'activityList': activityList,
                                                             'selectedActivity': selectedActivity,
                                                             'selectedMission':proj_mission,
                                                             'data_definition':data_definition})



# @login_required()
# def showAllProjects(request):
#
#     data_definition=DataDefinition.objects.all()
#
#     projects_list = []
#
#     if request.method == "GET":
#
#         # To get list of all Projects frm the Database
#         projects = list(Project.objects.all())
#
#         for x in projects:
#
#             # Finding the Mission of each project from ProjectMission Table
#             projmisn =ProjectMission.objects.filter(project_name_id=x.id).values('mission__mission_name','mission_type')
#
#             # Finding the Community Partner of each Project from ProjectCommunityPartner Table
#             proj_comm_par = ProjectCommunityPartner.objects.filter(project_name_id=x.id).values_list('community_partner__name', flat=True)
#
#             # Finding the Campus Partner of each Project from ProjectCampusPartner Table
#             proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=x.id).values_list('campus_partner__name',flat=True)
#
#             data = {'pk': x.pk, 'name': x.project_name.split(":")[0], 'engagementType': x.engagement_type,'academic_year' : x.academic_year,
#                     'activityType': x.activity_type,
#                     'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
#                     'description': x.description,
#                     'startDate': x.start_date,
#                     'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
#                     'total_uno_hours': x.total_uno_hours,
#                     'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
#                     'total_uno_faculty': x.total_uno_faculty,
#                     'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
#                     'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'comm_part': proj_comm_par,
#                     'camp_part': proj_camp_par
#                     }
#             projects_list.append(data)
#
#     return render(request, 'projects/allProjects.html', {'project': projects_list, 'data_definition':data_definition})


# @login_required()
# def showAllProjects(request):
#     selectedprojectId = request.GET.get('proj_id_list', None)
#     print('selectedprojectId--',selectedprojectId)
#     data_definition=DataDefinition.objects.all()
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
#     projects_list=[]
#     cursor = connection.cursor()
#     k12_selection = request.GET.get('k12_flag', None)
#     k12_init_selection = "All"
#     if k12_selection is None:
#         k12_selection = k12_init_selection
#
#     k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})
#
#     engagement_type_filter = request.GET.get('engagement_type', None)
#     if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
#         eng_type_cond = '%'
#     else:
#         eng_type_cond = engagement_type_filter
#
#     mission_type_filter = request.GET.get('mission', None)
#     if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
#         mission_type_cond = '%'
#     else:
#         mission_type_cond = mission_type_filter
#
#     community_type_filter = request.GET.get('community_type', None)
#     if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
#         community_type_cond = '%'
#     else:
#         community_type_cond = community_type_filter
#
#     campus_partner_filter = request.GET.get('campus_partner', None)
#     if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
#         campus_partner_cond = '%'
#         campus_id = 0
#     else:
#         campus_partner_cond = campus_partner_filter
#         campus_id = int(campus_partner_filter)
#
#     college_unit_filter = request.GET.get('college_name', None)
#     if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
#         college_unit_cond = '%'
#         campus_filter_qs = CampusPartner.objects.all()
#     else:
#         college_unit_cond = college_unit_filter
#         campus_filter_qs = CampusPartner.objects.filter(college_name_id=campus_partner_filter)
#     campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]
#
#
#     academic_year_filter = request.GET.get('academic_year', None)
#     acad_years = AcademicYear.objects.all()
#     yrs = []
#     for e in acad_years:
#         yrs.append(e.id)
#     max_yr_id = max(yrs)
#     print("max_yr_id", max_yr_id)
#     if academic_year_filter is None or academic_year_filter == '':
#         academic_start_year_cond = int(max_yr_id)
#         academic_end_year_cond = int(max_yr_id)
#
#     elif academic_year_filter == "All":
#         academic_start_year_cond = int(max_yr_id)
#         academic_end_year_cond = 1
#     else:
#         academic_start_year_cond = int(academic_year_filter)
#         academic_end_year_cond = int(academic_year_filter)
#
#     K12_filter = request.GET.get('k12_flag', None)
#     if K12_filter is None or K12_filter == "All" or K12_filter == '':
#         K12_filter_cond = '%'
#
#     elif K12_filter == 'Yes':
#         K12_filter_cond = 'true'
#
#     elif K12_filter == 'No':
#         K12_filter_cond = 'false'
#
#     cec_part_selection = request.GET.get('weitz_cec_part', None)
#     cec_part_init_selection = "All"
#     if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
#         cec_part_selection = cec_part_init_selection
#         cec_part_cond = '%'
#         params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
#                   K12_filter_cond, academic_start_year_cond, academic_end_year_cond]
#         cursor = connection.cursor()
#         cursor.execute(sql.all_projects_sql, params)
#         # cursor.execute(sql.projects_report, [project_ids])
#     elif cec_part_selection == "CURR_COMM":
#         cec_start_acad_year = academic_start_year_cond
#         cec_end_acad_year = academic_end_year_cond
#         params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
#                   K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_start_acad_year,
#                   cec_end_acad_year]
#         cursor = connection.cursor()
#         cursor.execute(sql.all_projects_cec_curr_comm_report_filter, params)
#     elif cec_part_selection == "FORMER_COMM":
#         cec_start_acad_year = academic_start_year_cond
#         cec_end_acad_year = academic_end_year_cond
#         params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
#                   K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_end_acad_year]
#         cursor = connection.cursor()
#         cursor.execute(sql.all_projects_cec_former_comm_report_filter, params)
#     elif cec_part_selection == "FORMER_CAMP":
#         cec_start_acad_year = academic_start_year_cond
#         cec_end_acad_year = academic_end_year_cond
#         params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
#                   K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_end_acad_year]
#         cursor = connection.cursor()
#         cursor.execute(sql.all_projects_cec_former_camp_report_filter, params)
#     elif cec_part_selection == "CURR_CAMP":
#         cec_start_acad_year = academic_start_year_cond
#         cec_end_acad_year = academic_end_year_cond
#         params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
#                   K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_start_acad_year,
#                   cec_end_acad_year]
#         cursor = connection.cursor()
#         cursor.execute(sql.all_projects_cec_curr_camp_report_filter, params)
#     # print('CEC Partner set in view ' + cec_part_selection)
#
#     cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
#     print("CEC partner condition: ", cec_part_selection)
#
#
#     if selectedprojectId is not None:
#         if selectedprojectId.find(",") != -1:
#             project_name_list = selectedprojectId.split(",")
#             print('project_name_list: ', str(tuple(project_name_list)))
#             cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
#                        params=None)
#            # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
#         else:
#             projId = "("+str(selectedprojectId)+")"
#             print('project_name_list--',projId)
#             cursor.execute(sqlfiles.showSelectedProjects(projId),
#                        params=None)
#             #cursor.execute(sql.search_projects_sql,project_name_list)
#     # else:
#     #
#     #     cursor.execute(sql.all_projects_sql)
#
#     for obj in cursor.fetchall():
#          projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
#                               "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
#                               "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
#                               "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18], "project_type": obj[19]
#                               , "end_semester": obj[20], "end_academic_year" : obj[21], "sub_category" : obj[22], "campus_lead_staff": obj[23]})
#     return render(request, 'projects/allProjects.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
#                    'campus_filter': campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
#                    'k12_choices': k12_choices, 'k12_selection': k12_selection,
#                    'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection})


#Show all projects login view


@login_required()
def showAllProjects(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    print('selectedprojectId--',selectedprojectId)
    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    status_draft = Status.objects.filter(name='Drafts')
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    # campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
    #     campus_partner_id__in=campus_filtered_ids))
    projects_list=[]
    cursor = connection.cursor()
    k12_selection = request.GET.get('k12_flag', None)
    # k12_init_selection = "All"
    # if k12_selection is None:
        # k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_cond)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

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
    print("default_yr_id---", default_yr_id)
    print ("max_yr ---", max_yr_id)
    if academic_year_filter is None or academic_year_filter == '':
        academic_start_year_cond = int(default_yr_id)
        academic_end_year_cond = int(default_yr_id)

    elif academic_year_filter == "All":
        academic_start_year_cond = int(max_yr_id)
        academic_end_year_cond = 1
    else:
        academic_start_year_cond = int(academic_year_filter)
        academic_end_year_cond = int(academic_year_filter)

    print("academic_start_year_cond----", academic_start_year_cond)
    print("academic_end_year_cond---", academic_end_year_cond)

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond = 'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    cec_part_init_selection = "All"
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

    params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
              K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql, params)

    # if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
    #     cec_part_selection = cec_part_init_selection
    #     cec_part_cond = '%'
    #     params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
    #               K12_filter_cond, academic_start_year_cond, academic_end_year_cond]
    #     cursor = connection.cursor()
    #     cursor.execute(sql.all_projects_sql, params)
    #     # cursor.execute(sql.projects_report, [project_ids])
    # elif cec_part_selection == "CURR_COMM":
    #     cec_start_acad_year = academic_start_year_cond
    #     cec_end_acad_year = academic_end_year_cond
    #     params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
    #               K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_start_acad_year,
    #               cec_end_acad_year]
    #     cursor = connection.cursor()
    #     cursor.execute(sql.all_projects_cec_curr_comm_report_filter, params)
    # elif cec_part_selection == "FORMER_COMM":
    #     cec_start_acad_year = academic_start_year_cond
    #     cec_end_acad_year = academic_end_year_cond
    #     params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
    #               K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_end_acad_year]
    #     cursor = connection.cursor()
    #     cursor.execute(sql.all_projects_cec_former_comm_report_filter, params)
    # elif cec_part_selection == "FORMER_CAMP":
    #     cec_start_acad_year = academic_start_year_cond
    #     cec_end_acad_year = academic_end_year_cond
    #     params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
    #               K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_end_acad_year]
    #     cursor = connection.cursor()
    #     cursor.execute(sql.all_projects_cec_former_camp_report_filter, params)
    # elif cec_part_selection == "CURR_CAMP":
    #     cec_start_acad_year = academic_start_year_cond
    #     cec_end_acad_year = academic_end_year_cond
    #     params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
    #               K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_start_acad_year,
    #               cec_end_acad_year]
    #     cursor = connection.cursor()
    #     cursor.execute(sql.all_projects_cec_curr_camp_report_filter, params)
    # # print('CEC Partner set in view ' + cec_part_selection)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
    print("CEC partner condition: ", cec_part_selection)


    if selectedprojectId is not None:
        if selectedprojectId.find(",") != -1:
            project_name_list = selectedprojectId.split(",")
            print('project_name_list: ', str(tuple(project_name_list)))
            cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
                       params=None)
           # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
        else:
            projId = "("+str(selectedprojectId)+")"
            print('project_name_list--',projId)
            cursor.execute(sqlfiles.showSelectedProjects(projId),
                       params=None)
            #cursor.execute(sql.search_projects_sql,project_name_list)
    # else:
    #
    #     cursor.execute(sql.all_projects_sql)

    for obj in cursor.fetchall():
         projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
                              "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
                              "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
                              "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18], "project_type": obj[19]
                              , "end_semester": obj[20], "end_academic_year" : obj[21], "sub_category" : obj[22], "campus_lead_staff": obj[23],
                               "mission_image": obj[24], "other_activity_type": obj[25]})
    return render(request, 'projects/allProjects.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
                   'campus_filter': campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
                   'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,'projects': project_filter})



# all projects ends here


@login_required()
def SearchForProjectAdd(request,pk):
    foundProject = None
    names = []

    for project in Project.objects.all():
        names.append(project.project_name)

    campusUserProjectsNames = []
    campusPartnerProjects = ProjectCampusPartner.objects.all()
    for project in ProjectCampusPartner.objects.all():
        campusUserProjectsNames.append(project.project_name)

    for project in Project.objects.all():
        if project.pk == int(pk):
            foundProject = project

    cp = CampusPartnerUser.objects.filter(user_id=request.user.id)[0].campus_partner
    object = ProjectCampusPartner(project_name=foundProject, campus_partner=cp)
    object.save()
    return redirect("myProjects")


#Public reports start here
#New view for project public table and card view
def projectstablePublicReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    print('selectedprojectId--',selectedprojectId)
    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    status_draft = Status.objects.filter(name='Drafts')
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))
    projects_list=[]
    cursor = connection.cursor()
    k12_selection = request.GET.get('k12_flag', None)
    # k12_init_selection = "All"
    # if k12_selection is None:
    #     k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_cond)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]


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

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond = 'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    cec_part_init_selection = "All"
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

    params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
              K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql, params)


    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
    print("CEC partner condition: ", cec_part_selection)

    if selectedprojectId is not None:
        if selectedprojectId.find(",") != -1:
            project_name_list = selectedprojectId.split(",")
            print('project_name_list: ', str(tuple(project_name_list)))
            cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
                           params=None)
        # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
        else:
            projId = "(" + str(selectedprojectId) + ")"
            print('project_name_list--', projId)
            cursor.execute(sqlfiles.showSelectedProjects(projId),
                           params=None)
            # cursor.execute(sql.search_projects_sql,project_name_list)
    # else:
    #
    #     cursor.execute(sql.all_projects_sql)

    for obj in cursor.fetchall():
        projects_list.append(
            {"name": obj[0].split("(")[0], "projmisn": obj[1], "comm_part": obj[2], "camp_part": obj[3],
             "engagementType": obj[4], "academic_year": obj[5], "semester": obj[6], "status": obj[7], "startDate": obj[8], "endDate": obj[9], "outcomes": obj[10],
             "total_uno_students": obj[11], "total_uno_hours": obj[12], "total_uno_faculty": obj[13], "total_k12_students": obj[14],
             "total_k12_hours": obj[15], "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18],
             "project_type": obj[19], "end_semester": obj[20], "end_academic_year": obj[21], "sub_category": obj[22],
             "campus_lead_staff": obj[23], "mission_image": obj[24], "other_activity_type": obj[25]})
    return render(request, 'reports/projectspublictableview.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
                   'campus_filter': campus_project_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
                   'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,'projects': project_filter})



def projectsPublicReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    print('selectedprojectId--',selectedprojectId)
    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    status_draft = Status.objects.filter(name='Drafts')
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))
    projects_list=[]
    cursor = connection.cursor()
    k12_selection = request.GET.get('k12_flag', None)
    # k12_init_selection = "All"
    # if k12_selection is None:
    #     k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_cond)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]


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

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond = 'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    cec_part_init_selection = "All"
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

    params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
              K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql, params)


    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
    print("CEC partner condition: ", cec_part_selection)

    if selectedprojectId is not None and selectedprojectId != '':
        if selectedprojectId.find(",") != -1:
            project_name_list = selectedprojectId.split(",")
            print('project_name_list: ', str(tuple(project_name_list)))
            cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
                           params=None)
        # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
        else:
            projId = "(" + str(selectedprojectId) + ")"
            print('project_name_list--', projId)
            cursor.execute(sqlfiles.showSelectedProjects(projId),
                           params=None)
            # cursor.execute(sql.search_projects_sql,project_name_list)
    # else:
    #
    #     cursor.execute(sql.all_projects_sql)

    for obj in cursor.fetchall():
         projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
                              "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
                              "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
                              "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18], "project_type": obj[19]
                              , "end_semester": obj[20], "end_academic_year" : obj[21], "sub_category" : obj[22], "campus_lead_staff": obj[23],
                               "mission_image": obj[24], "other_activity_type": obj[25]})
    page = request.GET.get('page', 1)
    paginator = Paginator(projects_list, 5)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    return render(request, 'reports/projects_public_view.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
                   'campus_filter': campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
                   'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,'projects': project_filter, 'cards':cards})


# project private card and table view starts here

@login_required()
def projectsPrivateReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    print('selectedprojectId--',selectedprojectId)

    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    status_draft = Status.objects.filter(name='Drafts')
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)

    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))

    projects_list = []
    cursor = connection.cursor()
    k12_selection = request.GET.get('k12_flag', None)
    # k12_init_selection = "All"
    # if k12_selection is None:
    #     k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_cond)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

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

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond = 'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    cec_part_init_selection = "All"
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

    params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
              K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql, params)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
    print("CEC partner condition: ", cec_part_selection)

    if selectedprojectId is not None:
        if selectedprojectId.find(",") != -1:
            project_name_list = selectedprojectId.split(",")
            print('project_name_list: ', str(tuple(project_name_list)))
            cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
                           params=None)
        # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
        else:
            projId = "(" + str(selectedprojectId) + ")"
            print('project_name_list--', projId)
            cursor.execute(sqlfiles.showSelectedProjects(projId),
                           params=None)

    for obj in cursor.fetchall():
         projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
                              "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
                              "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
                              "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18], "project_type": obj[19]
                              , "end_semester": obj[20], "end_academic_year" : obj[21], "sub_category" : obj[22], "campus_lead_staff": obj[23],
                               "mission_image": obj[24], "other_activity_type": obj[25]})
    page = request.GET.get('page', 1)
    paginator = Paginator(projects_list, 5)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    return render(request, 'reports/projects_private_view.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
                   'campus_filter': campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
                   'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,'projects': project_filter, 'cards':cards})

@login_required()
def projectstablePrivateReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    print('selectedprojectId--',selectedprojectId)
    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    status_draft = Status.objects.filter(name='Drafts')
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__in=status_draft))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))
    # projects_list=[]
    cursor = connection.cursor()
    k12_selection = request.GET.get('k12_flag', None)
    # k12_init_selection = "All"
    # if k12_selection is None:
    #     k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is None or engagement_type_filter == "All" or engagement_type_filter == '':
        eng_type_cond = '%'
    else:
        eng_type_cond = engagement_type_filter

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is None or mission_type_filter == "All" or mission_type_filter == '':
        mission_type_cond = '%'
    else:
        mission_type_cond = mission_type_filter

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is None or community_type_filter == "All" or community_type_filter == '':
        community_type_cond = '%'
    else:
        community_type_cond = community_type_filter

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is None or campus_partner_filter == "All" or campus_partner_filter == '':
        campus_partner_cond = '%'
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()
    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_cond)
    campus_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

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

    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter is None or K12_filter == "All" or K12_filter == '':
        K12_filter_cond = '%'

    elif K12_filter == 'Yes':
        K12_filter_cond = 'true'

    elif K12_filter == 'No':
        K12_filter_cond = 'false'

    cec_part_init_selection = "All"
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

    params = [eng_type_cond, mission_type_cond, community_type_cond, campus_partner_cond, college_unit_cond,
              K12_filter_cond, academic_start_year_cond, academic_end_year_cond, cec_comm_part_cond, cec_camp_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql, params)

    cec_part_choices = CecPartChoiceForm(initial={'cec_choice': cec_part_selection})
    print("CEC partner condition: ", cec_part_selection)

    if selectedprojectId is not None:
        if selectedprojectId.find(",") != -1:
            project_name_list = selectedprojectId.split(",")
            print('project_name_list: ', str(tuple(project_name_list)))
            cursor.execute(sqlfiles.showSelectedProjects(tuple(project_name_list)),
                           params=None)
        # cursor.execute(sql.search_projects_sql,str(tuple(project_name_list)))
        else:
            projId = "(" + str(selectedprojectId) + ")"
            print('project_name_list--', projId)
            cursor.execute(sqlfiles.showSelectedProjects(projId),
                           params=None)

    for obj in cursor.fetchall():
         projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
                              "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
                              "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
                              "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18], "project_type": obj[19]
                              , "end_semester": obj[20], "end_academic_year" : obj[21], "sub_category" : obj[22], "campus_lead_staff": obj[23],
                               "mission_image": obj[24], "other_activity_type": obj[25]})
    return render(request, 'reports/projectsprivatetableview.html', {'project': projects_list, 'data_definition':data_definition, "missions": missions, "communityPartners": communityPartners,
                   'campus_filter': campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id,
                   'k12_choices': k12_choices, 'k12_selection': k12_selection,
                   'cec_part_choices': cec_part_choices, 'cec_part_selection': cec_part_selection,'projects': project_filter})


#Project private reports card and table view end here.



def projectsfromMissionReport(request, pk):
        proj_id_list = request.GET.get('proj_id_list', None)
        #type = request.GET.get('type', None)
        data_list = []
        legislative_choices = []
        legislative_search = ''
        data_definition = DataDefinition.objects.all()

        # set legislative_selection on template choices field -- Manu Start
        legislative_selection = request.GET.get('legislative_value', None)

        if legislative_selection is None:
            legislative_selection = 'All'

        legislative_choices.append('All')
        for i in range(1, 50):
            legistalive_val = 'Legislative District ' + str(i)
            legislative_choices.append(legistalive_val)

        if legislative_selection is not None and legislative_selection != 'All':
            legislative_search = legislative_selection.split(" ")[2]

        # set legislative_selection on template choices field -- Manu End
        k12_selection = request.GET.get('k12_flag', None)
        k12_init_selection = "All"
        if k12_selection is None:
            k12_selection = k12_init_selection

        k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})
        if proj_id_list is None:
            pk = None
            if k12_selection == 'Yes':
                if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                    project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True))
                else:
                    project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True).filter(
                        legislative_district=legislative_search))
            elif k12_selection == 'No':
                if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                    project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False))
                else:
                    project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False).filter(
                        legislative_district=legislative_search))
            else:
                if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
                else:
                    project_filter = ProjectFilter(request.GET,
                                                   queryset=Project.objects.filter(
                                                       legislative_district=legislative_search))

            missions = ProjectMissionFilter(request.GET,
                                            queryset=ProjectMission.objects.filter(mission_type='Primary').filter(mission_id=pk))

        # else:
        #     project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(project_name__in=proj_id_list))
        #     missions = ProjectMissionFilter(request.GET,queryset=ProjectMission.objects.filter(mission_type='Primary').filter(mission_id=pk))
        #
        # # set k12 flag on template choices field


        else:
            if proj_id_list.find(",") != -1:
                project_name_list =proj_id_list.split(",")
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id__in=project_name_list))
            else:
                project_name_list = proj_id_list
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id=project_name_list))

        # set k12 flag on template choices field

        if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        else:
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
                legislative_district=legislative_search))
        # legislative district end -- Manu
        campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

        community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
        community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
            community_partner_id__in=community_filtered_ids))
        if pk is None:
             missions = ProjectMissionFilter(request.GET,queryset=ProjectMission.objects.filter(mission_type='Primary'))
        else:
             missions = ProjectMissionFilter(request.GET,queryset=ProjectMission.objects.filter(mission_type='Primary').filter(mission_id=pk))

        campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

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
        projects_comm_ids = list(set(proj_ids1).difference(set(project_ids)))
        # projects_comm = list(Project.objects.filter(id__in=projects_comm_ids))

        #List of all Projects with Campus, Community Partners and have Mission
        # projects = list(Project.objects.filter(id__in=project_ids))
        cursor = connection.cursor()
        cursor.execute(sql.projects_report, [project_ids])

        for obj in cursor.fetchall():
            data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                              "engagementType": obj[3]})
        k12_selection = request.GET.get('k12_flag', None)
        if k12_selection is None:
            k12_selection = k12_init_selection

        b = request.GET.get('community_type', None)
        c = request.GET.get('weitz_cec_part', None)
        k12_selection = request.GET.get('k12_flag', None)
        if k12_selection is None:
            k12_selection = k12_init_selection
        #print('K12 flag selected in page ' + k12_selection)
        if b is None or b == "All" or b == '':
            if c is None or c == "All" or c == '':
                if k12_selection is None or k12_selection == 'All' or k12_selection == '':
                    cursor.execute(sql.projects_report, [projects_comm_ids])

                # for obj in cursor.fetchall():
                #     data_list.append(
                #         {"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                #          "engagementType": obj[3]})

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

        return render(request, 'reports/projects_public_view.html',
                      {'projects': project_filter, 'data_definition': data_definition,
                       'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,
                       'k12_choices': k12_choices,
                       'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
                       "campus_filter": campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id})
#                     for obj in cursor.fetchall():
#                         data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
#                             "engagementType": obj[3]})
# >>>>>>> 29f42791314d16a725b2d0e47474d1ba325a412d
#
#         return render(request, 'reports/projects_private_view.html',
#                     {'projects': project_filter, 'data_definition': data_definition,
#                     'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
#                     'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
#                     "campus_filter": campus_project_filter, 'college_filter': campusPartners,
#                     "k12_choices": k12_choices,
#                     "k12_selection": k12_selection})

# List of community Partners Public View

def projectsfromEngagementReport(request):
    proj_id_list = request.GET.get('proj_id_list', None)
    print ('proj_id_list: ', proj_id_list)
    # type = request.GET.get('type', None)
    data_list = []
    legislative_choices = []
    legislative_search = ''
    data_definition = DataDefinition.objects.all()

    # set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    # set legislative_selection on template choices field -- Manu End
    k12_selection = request.GET.get('k12_flag', None)
    k12_init_selection = "All"
    if k12_selection is None:
        k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})
    if proj_id_list is None:
        # project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter())

        if k12_selection == 'Yes':
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True))
            else:
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True).filter(
                    legislative_district=legislative_search))
        elif k12_selection == 'No':
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False))
            else:
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False).filter(
                    legislative_district=legislative_search))
        else:
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
            else:
                project_filter = ProjectFilter(request.GET,
                                               queryset=Project.objects.filter(
                                                   legislative_district=legislative_search))

        #missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary')

    else:
        if proj_id_list.find(",") != -1:
            project_name_list = proj_id_list.split(",")
            print('project_name_list: ', project_name_list)
            project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id__in=project_name_list))
            print ('project_filter in eng_proj report', project_filter.qs.values_list('id', flat=True))
        else:
            project_name_list = proj_id_list
            project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id=project_name_list))

    # set k12 flag on template choices field

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
            legislative_district=legislative_search))
    # legislative district end -- Manu
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
    community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
        community_partner_id__in=community_filtered_ids))

    missions = ProjectMissionFilter(request.GET,
                                        queryset=ProjectMission.objects.filter(mission_type='Primary'))

    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
    # community_filtered_ids = [community.id for community in communityPartners.qs]
    community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
        community_partner_id__in=community_filtered_ids))
    # community_project_filtered_ids = [project.project_name_id for project in community_project_filter.qs]
    community_project_filtered_ids = community_project_filter.qs.values_list('project_name', flat=True)

    campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))
    # campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    mission_filtered_ids = missions.qs.values_list('project_name', flat=True)
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)

    # Finding intersection of all the filters
    proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    proj_ids2 = list(set(proj_ids1).intersection(project_filtered_ids))
    project_ids = list(set(proj_ids2).intersection(community_project_filtered_ids))

    # To get the projects which does not have community partners
    projects_comm_ids = list(set(proj_ids1).difference(set(project_ids)))
    # projects_comm = list(Project.objects.filter(id__in=projects_comm_ids))

    # List of all Projects with Campus, Community Partners and have Mission
    # projects = list(Project.objects.filter(id__in=project_ids))
    project_ids_list = list(project_filtered_ids)
    cursor = connection.cursor()
    cursor.execute(sql.projects_report, [project_ids_list])

    for obj in cursor.fetchall():
        data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                          "engagementType": obj[3]})
    k12_selection = request.GET.get('k12_flag', None)
    if k12_selection is None:
        k12_selection = k12_init_selection

    b = request.GET.get('community_type', None)
    c = request.GET.get('weitz_cec_part', None)
    k12_selection = request.GET.get('k12_flag', None)
    if k12_selection is None:
        k12_selection = k12_init_selection
    # print('K12 flag selected in page ' + k12_selection)
    if b is None or b == "All" or b == '':
        if c is None or c == "All" or c == '':
            if k12_selection is None or k12_selection == 'All' or k12_selection == '':
                cursor.execute(sql.projects_report, [projects_comm_ids])

            # for obj in cursor.fetchall():
            #     data_list.append(
            #         {"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
            #          "engagementType": obj[3]})

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

    return render(request, 'reports/projects_public_view.html',
                  {'projects': project_filter, 'data_definition': data_definition,
                   'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,
                   'k12_choices': k12_choices,
                   'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
                   "campus_filter": campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id})


def projectsfromCommunityPartnerReport(request):
    proj_id_list = request.GET.get('proj_ids', None)
    # type = request.GET.get('type', None)
    data_list = []
    legislative_choices = []
    legislative_search = ''
    data_definition = DataDefinition.objects.all()

    # set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    # set legislative_selection on template choices field -- Manu End
    k12_selection = request.GET.get('k12_flag', None)
    k12_init_selection = "All"
    if k12_selection is None:
        k12_selection = k12_init_selection

    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})
    if proj_id_list is None:
        # project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter())
        #pk = None
        if k12_selection == 'Yes':
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True))
            else:
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=True).filter(
                    legislative_district=legislative_search))
        elif k12_selection == 'No':
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False))
            else:
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(k12_flag=False).filter(
                    legislative_district=legislative_search))
        else:
            if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
                project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
            else:
                project_filter = ProjectFilter(request.GET,
                                               queryset=Project.objects.filter(
                                                   legislative_district=legislative_search))

        missions = ProjectMissionFilter(request.GET,
                                        queryset=ProjectMission.objects.filter(mission_type='Primary'))


    else:
        if proj_id_list.find(",") != -1:
            project_name_list = proj_id_list.split(",")
            project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id__in=project_name_list))
        else:
            project_name_list = proj_id_list
            project_filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id=project_name_list))

    # set k12 flag on template choices field

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    else:
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
            legislative_district=legislative_search))
    # legislative district end -- Manu
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
    community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
        community_partner_id__in=community_filtered_ids))

    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))

    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    community_filtered_ids = communityPartners.qs.values_list('id', flat=True)
    # community_filtered_ids = [community.id for community in communityPartners.qs]
    community_project_filter = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.filter(
        community_partner_id__in=community_filtered_ids))
    # community_project_filtered_ids = [project.project_name_id for project in community_project_filter.qs]
    community_project_filtered_ids = community_project_filter.qs.values_list('project_name', flat=True)

    campus_filtered_ids = campusPartners.qs.values_list('id', flat=True)
    # campus_filtered_ids = [campus.id for campus in campusPartners.qs]
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(
        campus_partner_id__in=campus_filtered_ids))
    # campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    mission_filtered_ids = missions.qs.values_list('project_name', flat=True)
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)

    # Finding intersection of all the filters
    proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    proj_ids2 = list(set(proj_ids1).intersection(project_filtered_ids))
    project_ids = list(set(proj_ids2).intersection(community_project_filtered_ids))

    # To get the projects which does not have community partners
    projects_comm_ids = list(set(proj_ids1).difference(set(project_ids)))
    # projects_comm = list(Project.objects.filter(id__in=projects_comm_ids))

    # List of all Projects with Campus, Community Partners and have Mission
    # projects = list(Project.objects.filter(id__in=project_ids))
    cursor = connection.cursor()
    cursor.execute(sql.projects_report, [project_ids])

    for obj in cursor.fetchall():
        data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                          "engagementType": obj[3]})
    k12_selection = request.GET.get('k12_flag', None)
    if k12_selection is None:
        k12_selection = k12_init_selection

    b = request.GET.get('community_type', None)
    c = request.GET.get('weitz_cec_part', None)
    k12_selection = request.GET.get('k12_flag', None)
    if k12_selection is None:
        k12_selection = k12_init_selection
    # print('K12 flag selected in page ' + k12_selection)
    if b is None or b == "All" or b == '':
        if c is None or c == "All" or c == '':
            if k12_selection is None or k12_selection == 'All' or k12_selection == '':
                cursor.execute(sql.projects_report, [projects_comm_ids])

            # for obj in cursor.fetchall():
            #     data_list.append(
            #         {"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
            #          "engagementType": obj[3]})

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

    return render(request, 'reports/projects_public_view.html',
                  {'projects': project_filter, 'data_definition': data_definition,
                   'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,
                   'k12_choices': k12_choices,
                   'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
                   "campus_filter": campus_filter, 'college_filter': campusPartners, 'campus_id': campus_id})



def communityPublicReport(request):
    community_dict = {}
    community_list = []
    data_list=[]
    legislative_choices = []
    legislative_search = ''
    data_definition=DataDefinition.objects.all()
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    status_draft = Status.objects.filter(name='Drafts')

    comm_ids = request.GET.get('comm_ids', None)
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    for i in range(1,50):
        legistalive_val = 'Legislative District '+str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        if legislative_selection == '-1':
            legislative_search ='%'
        else:
            legislative_search = legislative_selection.split(" ")[2]

    college_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()

    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        legislative_district_cond = '%'

    else:
        legislative_district_cond = legislative_search

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

    #cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        # cec_part_selection = cec_part_init_selection
        cec_part_cond = '%'
        # cursor.execute(sql.projects_report, [project_ids])
    elif cec_part_selection == "CURR_COMM":
        cec_part_cond = 'Current'

    elif cec_part_selection == "FORMER_COMM":
        cec_part_cond = 'Former'

    if comm_ids is not None:
        print('list connn id --',len(comm_ids))
        params = []       
        if comm_ids.find(",") != -1:
            comm_list = comm_ids.split(",")
            params.append(tuple(comm_list))
            cursor = connection.cursor()
            cursor.execute(sql.selected_community_public_report, params)
            
        else:
            params.append(str(comm_ids))
            cursor = connection.cursor()
            cursor.execute(sql.selected_One_community_public_report, params)
        
    else:
        params = [community_type_cond, academic_start_year_cond, academic_end_year_cond, campus_partner_cond,
                  legislative_district_cond, college_unit_cond, cec_part_cond]
        cursor = connection.cursor()
        cursor.execute(sql.community_public_report, params)

    cec_part_choices = OommCecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    for obj in cursor.fetchall():
        print('project ids--',obj[6])
        proj_ids = obj[6]
        proj_idList = ''
        if proj_ids is not None:
            name_count = 0
            if len(proj_ids) > 0:
                for i in proj_ids:
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1
        
        data_list.append({"community_name": obj[0], "community_mission":obj[1],"project_count": obj[2], "project_id_list": proj_idList, "website": obj[3], "CommStatus": obj[4]})

    return render(request, 'reports/community_public_view.html', { 'college_filter': college_partner_filter, 'campus_filter': campus_project_filter,
                                                                'project_filter': project_filter,
                                                                'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 'communityData': data_list,
                                                                 'data_definition':data_definition,
                                                                 'campus_id':campus_id,
                                                                 'cec_part_choices': cec_part_choices})


@login_required()
def communityPrivateReport(request):
    community_dict = {}
    data_list = []
    community_list = []
    legislative_choices = []
    legislative_search = ''
    # comp_part_contact = []
    data_definition=DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    #set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    # legislative_choices.append('All')
    for i in range(1,50):
        legistalive_val = 'Legislative District '+str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        if legislative_selection == '-1':
            legislative_search ='%'
        else:
            legislative_search = legislative_selection.split(" ")[2]

    college_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    project_filtered_ids = project_filter.qs.values_list('id', flat=True)
    
    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is None or college_unit_filter == "All" or college_unit_filter == '':
        college_unit_cond = '%'
        campus_filter_qs = CampusPartner.objects.all()

    else:
        college_unit_cond = college_unit_filter
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_unit_filter)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
        legislative_district_cond = '%'

    else:
        legislative_district_cond = legislative_search

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
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        # cec_part_selection = cec_part_init_selection
        cec_part_cond = '%'
        # cursor.execute(sql.projects_report, [project_ids])
    elif cec_part_selection == "CURR_COMM":
        cec_part_cond = 'Current'

    elif cec_part_selection == "FORMER_COMM":
        cec_part_cond = 'Former'


    params = [community_type_cond, academic_start_year_cond, academic_end_year_cond, campus_partner_cond,
              legislative_district_cond, college_unit_cond, cec_part_cond]
    cursor = connection.cursor()
    cursor.execute(sql.community_private_report, params)
   
    cec_part_choices = OommCecPartChoiceForm(initial={'cec_choice': cec_part_selection})

    for obj in cursor.fetchall():
        print('proj ids--',obj[6])
        proj_ids = obj[6]
        proj_idList = ''
        if proj_ids is not None:
            name_count = 0
            if len(proj_ids) > 0:
                for i in proj_ids:
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        data_list.append({"CommunityName": obj[0], "mission":obj[1],"Projects": obj[2], "numberofunostudents": obj[3],
                          "unostudentshours": obj[4], "website": obj[5], "proj_id_list": proj_idList, "CommStatus": obj[7]})

    return render(request, 'reports/community_private_view.html', {'college_filter': college_partner_filter,'project_filter': project_filter,'data_definition':data_definition,
                                                                 'legislative_choices':legislative_choices, 'legislative_value':legislative_selection,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 'communityData': data_list,
                                                                   'campus_filter': campus_project_filter, 'campus_id':campus_id, 'cec_part_choices': cec_part_choices})


def communityfromMissionReport(request, pk):

    print('hit comm mission report')
    comm_ids = request.GET.get('comm_ids', None)

    legislative_choices = []
    legislative_search = ''
    # comp_part_contact = []
    data_definition = DataDefinition.objects.all()

    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    # set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    # project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
          project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    else:
         project_filter = ProjectFilter(request.GET,
                                       queryset=Project.objects.filter(legislative_district=legislative_search))
    # legislative district end -- Manu


    community_dict = {}
    community_list = []


    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    if comm_ids is None:
        community_mission = CommunityPartnerMission.objects.filter(mission_area_id=pk). \
            filter(mission_type='Primary').values_list('community_partner_id', flat=True)
        if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
                id__in=community_mission))
        else:
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
                id__in=community_mission).filter(legislative_district=legislative_search))

        #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(id__in=community_mission))

    else:
        if comm_ids.find(",") != -1:
            comm_list =comm_ids.split(",")
            communityPartners = communityPartnerFilter(request.GET,
                                                       queryset=CommunityPartner.objects.filter(id__in=comm_list))
        else:
            comm_list = comm_ids
            communityPartners = communityPartnerFilter(request.GET,
                                                       queryset=CommunityPartner.objects.filter(id=comm_list))

    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_partner_filtered_ids = campus_partner_filter.qs.values_list('id', flat=True)
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    project_filtered_ids = project_filter.qs.values_list('id', flat=True)
    print(project_filtered_ids)

    # proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    project_ids = list(set(campus_project_filtered_ids).intersection(project_filtered_ids))
    print(project_ids)

    for m in communityPartners.qs:
        proj_comm_par = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).values_list('project_name',flat=True)
        project_count = len(set(project_ids).intersection(proj_comm_par))
        #if project_count==0:
        #    continue
        # if type == 'mission':
        #     community_mission = CommunityPartnerMission.objects.filter(community_partner_id=m.id).\
        #         filter(mission_type='Primary', mission_area_id=pk).values_list('mission_area__mission_name', flat=True)
        # else:
        community_mission = CommunityPartnerMission.objects.filter(community_partner_id=m.id).\
            filter(mission_type='Primary').values_list('mission_area__mission_name', flat=True)
        community_dict['community_name'] = m.name
        community_dict['community_mission'] = community_mission
        community_dict['website'] = m.website_url
        community_dict['project_count'] = project_count

        # Code to get the contact email id of community partners from Contacts Model
        # contact = list(Contact.objects.filter(community_partner=m.id, contact_type='Primary'))
        # for contact in contact:
        #     comp_part_contact.append(contact.email_id)
        # list_contacts = comp_part_contact
        # comp_part_contact = []
        # community_dict['email'] = list_contacts

        # Code to get the uno hours, students, economic impact form Project Table
        total_uno_students = 0
        total_uno_hours = 0
        total_economic_impact= 0
        p_community = list(set(project_ids).intersection(proj_comm_par))
        for pm in p_community:
            uno_students = Project.objects.filter(id=pm).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm).aggregate(Sum('total_uno_hours'))
            economic_impact = Project.objects.filter(id=pm).aggregate(Sum('total_economic_impact'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
            total_economic_impact += economic_impact['total_economic_impact__sum']
        community_dict['total_uno_hours'] = total_uno_hours
        community_dict['total_uno_students'] = total_uno_students
        community_dict['total_economic_impact'] = total_economic_impact
        community_list.append(community_dict.copy())

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)

    return render(request, 'reports/community_private_view.html', {'college_filter': campus_partner_filter,'project_filter': project_filter,'data_definition':data_definition,
                                                                   'legislative_choices': legislative_choices,
                                                                   'legislative_value': legislative_selection,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 # 'missions': missions,
                                                                   'campus_filter': campus_project_filter, 'campus_id':campus_id})



def communityfromEngagementReport(request):

    print('hit comm engagemenet report')
    comm_ids = request.GET.get('comm_ids', None)
    print ('comm_ids:', comm_ids)

    legislative_choices = []
    legislative_search = ''
    # comp_part_contact = []
    data_definition = DataDefinition.objects.all()

    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    # set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        legislative_search = legislative_selection.split(" ")[2]

    # project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
          project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    else:
         project_filter = ProjectFilter(request.GET,
                                       queryset=Project.objects.filter(legislative_district=legislative_search))
    # legislative district end -- Manu


    community_dict = {}
    community_list = []


    #project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())

    if comm_ids is None:
        community_mission = CommunityPartnerMission.objects. filter(mission_type='Primary')\
            .values_list('community_partner_id', flat=True)
        if legislative_selection is None or legislative_selection == "All" or legislative_selection == '':
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
                id__in=community_mission))
        else:
            communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(
                id__in=community_mission).filter(legislative_district=legislative_search))

        #communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(id__in=community_mission))

    else:
        if comm_ids.find(",") != -1:
            comm_list = comm_ids.split(",")
            communityPartners = communityPartnerFilter(request.GET,
                                                       queryset=CommunityPartner.objects.filter(id__in=comm_list))
        else:
            comm_list = comm_ids
            communityPartners = communityPartnerFilter(request.GET,
                                                       queryset=CommunityPartner.objects.filter(id=comm_list))

    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_partner_filtered_ids = campus_partner_filter.qs.values_list('id', flat=True)
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    project_filtered_ids = project_filter.qs.values_list('id', flat=True)
    print(project_filtered_ids)

    # proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    project_ids = list(set(campus_project_filtered_ids).intersection(project_filtered_ids))
    print(project_ids)

    for m in communityPartners.qs:
        proj_comm_par = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).values_list('project_name',flat=True)
        project_count = len(set(project_ids).intersection(proj_comm_par))
        community_mission = CommunityPartnerMission.objects.filter(community_partner_id=m.id).\
            filter(mission_type='Primary').values_list('mission_area__mission_name', flat=True)
        community_dict['community_name'] = m.name
        community_dict['community_mission'] = community_mission
        community_dict['website'] = m.website_url
        community_dict['project_count'] = project_count

        # Code to get the contact email id of community partners from Contacts Model
        # contact = list(Contact.objects.filter(community_partner=m.id, contact_type='Primary'))
        # for contact in contact:
        #     comp_part_contact.append(contact.email_id)
        # list_contacts = comp_part_contact
        # comp_part_contact = []
        # community_dict['email'] = list_contacts

        # Code to get the uno hours, students, economic impact form Project Table
        total_uno_students = 0
        total_uno_hours = 0
        total_economic_impact= 0
        p_community = list(set(project_ids).intersection(proj_comm_par))
        for pm in p_community:
            uno_students = Project.objects.filter(id=pm).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm).aggregate(Sum('total_uno_hours'))
            economic_impact = Project.objects.filter(id=pm).aggregate(Sum('total_economic_impact'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
            total_economic_impact += economic_impact['total_economic_impact__sum']
        community_dict['total_uno_hours'] = total_uno_hours
        community_dict['total_uno_students'] = total_uno_students
        community_dict['total_economic_impact'] = total_economic_impact
        community_list.append(community_dict.copy())

    college_value = request.GET.get('college_name', None)
    if college_value is None or college_value == "All" or college_value == '':
        campus_filter_qs = CampusPartner.objects.all()
    else:
        campus_filter_qs = CampusPartner.objects.filter(college_name_id=college_value)
    campus_project_filter = [{'name': m.name, 'id': m.id} for m in campus_filter_qs]

    campus_id = request.GET.get('campus_partner')
    if campus_id == "All":
        campus_id = -1
    if (campus_id is None or campus_id == ''):
        campus_id = 0
    else:
        campus_id = int(campus_id)

    return render(request, 'reports/community_private_view.html', {'college_filter': campus_partner_filter,'project_filter': project_filter,'data_definition':data_definition,
                                                                   'legislative_choices': legislative_choices,
                                                                   'legislative_value': legislative_selection,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 # 'missions': missions,
                                                                   'campus_filter': campus_project_filter, 'campus_id':campus_id})


# project duplication check
def checkProject(request):
    data_list = [];
    flag = 0;
    data_definition = DataDefinition.objects.all()
    academic_yr_filter = AcademicYear.objects.all().order_by('-academic_year')
    campus_filter = CampusPartner.objects.all()
    Community_filter = CommunityPartner.objects.all()

    if request.method == 'POST':
        flag = 0;
        projectName = request.POST['projectName'].strip()
        communityPartner = request.POST.get('communityPartner').replace('-', '')
        campusPartner = request.POST['campusPartner'].replace('-', '')
        academicYear = request.POST['academicYear'].replace('---', '')
        #  academic_filter_qs = AcademicYear.objects.get(academic_year=academicYear)
        #  acad = academic_filter_qs.id
        #  acad_id = str(acad)
        # # acad_id = [m.id for m in academic_filter_qs]
        #  print(acad_id)
        print(academicYear)
        print(sqlfiles.checkProjectsql(projectName, communityPartner, campusPartner, academicYear))
        cursor = connection.cursor()
        cursor.execute(sqlfiles.checkProjectsql(projectName, communityPartner, campusPartner, academicYear),
                       params=None)
        rows = cursor.fetchall()
        # print(rows[0][0])
        if (rows != []):

            for obj in rows:

                if (projectName.strip().lower() in obj[0].split("(")[0].strip().lower()):
                    flag = 2

                if (projectName.strip().lower() == obj[0].split("(")[0].strip().lower()):
                    flag = 1

                data_list.append(
                    {"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[3],
                     "academicYear": obj[2], 'flagBit': flag})

            return render(request, 'projects/checkProject.html',
                          {'data_list': data_list, "projectName": projectName, 'flagBit': flag,
                           'data_definition': data_definition,
                           'academic_yr_filter': academic_yr_filter,
                           'campus_filter': campus_filter,
                           "Community_filter": Community_filter,
                           'communityPartner_selected': communityPartner,
                           'campusPartner_selected': campusPartner,
                           'academicYear_selected': academicYear
                           })

        else:

            data_list.append({"projectName": "", "communityPartner": "", "campusPartner": "",
                              "academicYear": "", 'flagBit': flag})
            return render(request, 'projects/checkProject.html',
                          {'data_list': data_list, "projectName": projectName, 'flagBit': flag,
                           'data_definition': data_definition,
                           'academic_yr_filter': academic_yr_filter,
                           'campus_filter': campus_filter,
                           "Community_filter": Community_filter,
                           'communityPartner_selected': communityPartner,
                           'campusPartner_selected': campusPartner,
                           'academicYear_selected': academicYear
                           })
    else:

        return render(request, 'projects/checkProject.html',
                      {'data_list': data_list,
                       'data_definition': data_definition, 'academic_yr_filter': academic_yr_filter,
                       'campus_filter': campus_filter, "Community_filter": Community_filter})


@login_required()
# @campuspartner_required()
def project_total_Add(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    secondary_mission_details = modelformset_factory(ProjectMission, extra=1, form=ScndProjectMissionFormset)
    sub_category = modelformset_factory(ProjectSubCategory, extra=1, form=AddSubCategoryForm)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition=DataDefinition.objects.all()
    if request.method == 'POST':
        # cache.clear()
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None, prefix='mission')
        categoryformset = sub_category(request.POST or None, prefix='sub_category')
        formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        # print("validation ststus:",project.is_valid() , formset.is_valid() ,course.is_valid() , formset2.is_valid())
        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid() and formset3.is_valid() and formset4.is_valid() and categoryformset.is_valid():
            ##Convert address to cordinates and save the legislatve district and household income
            a = 0
            project.total_uno_hours = a
            proj = project.save()
            proj.project_name = proj.project_name + " :" + str(proj.academic_year)
            eng = str(proj.engagement_type)
            if eng == "Service Learning":
                course = course.save(commit=False)
                course.project_name = proj
                course.save()
            address = proj.address_line1
            address = proj.address_line1
            # if (address != "N/A"):  # check if a community partner's address is there
            #     fulladdress = proj.address_line1 + ' ' + proj.city
            #     geocode_result = gmaps.geocode(fulladdress)  # get the coordinates
            #     proj.latitude = geocode_result[0]['geometry']['location']['lat']
            #     proj.longitude = geocode_result[0]['geometry']['location']['lng']
            #     #### checking lat and long are incorrect
            #     if (proj.latitude == '0') or (proj.longitude == '0'):
            #         project = ProjectFormAdd()
            #         course = CourseForm()
            #         formset = mission_details(queryset=ProjectMission.objects.none())
            #         formset4 = secondary_mission_details(queryset=ProjectMission.objects.none())
            #         # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
            #         formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
            #         return render(request, 'projects/createProject.html',
            #                       {'project': project, 'formset': formset, 'formset4': formset4, 'formset3': formset3,
            #                        'course': course})
            # proj.save()
            # coord = Point([proj.longitude, proj.latitude])
            # for i in range(len(district)):  # iterate through a list of district polygons
            #     property = district[i]
            #     polygon = shape(property['geometry'])  # get the polygons
            #     if polygon.contains(coord):  # check if a partner is in a polygon
            #         proj.legislative_district = property["id"]  # assign the district number to a partner
            #         proj.save()
            # for m in range(len(countyData)):  # iterate through the County Geojson
            #     properties2 = countyData[m]
            #     polygon = shape(properties2['geometry'])  # get the polygon
            #     if polygon.contains(coord):  # check if the partner in question belongs to a polygon
            #         proj.county = properties2['properties']['NAME']
            #         proj.median_household_income = properties2['properties']['Income']
            #         proj.save()
            mission_form = formset.save(commit=False)
            secondary_mission_form = formset4.save(commit=False)
            proj_comm_form = formset2.save(commit=False)
            sub_cat_form = categoryformset.save(commit=False)
            proj_campus_form = formset3.save(commit=False)
            for k in proj_comm_form:
                k.project_name = proj
                print("in add comm")
                print(k.project_name)
                print(k.total_hours, k.total_people)
                k.save()

            for cat in sub_cat_form:
                cat.project_name = proj
                print("in add sub category")
                print(cat.project_name)
                cat.save()

            for form in mission_form:
                form.project_name = proj
                #print("in add mission")
                form.mission_type = 'Primary'
                form.save()


            for form4 in secondary_mission_form:
                form4.project_name = proj
                #print("in add secondary mission")
                form4.mission_type = 'Other'
                form4.save()

            # projh = Project.objects.get(pk=project_name_id.pk)
            init = 0
            t = 0
            for c in proj_campus_form:
                c.project_name = proj
                print('totalhrs')
                print(c.total_hours, c.total_people)
                c.save()
                # init = proj.total_uno_hours
                t += c.total_hours * c.total_people
                print(t)
                proj.total_uno_hours = t
                proj.save()
                print(c.total_hours)
            projects_list = []
            camp_part_names = []
            p = 0
            # Get the campus partner id related to the user
            camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
            for c in camp_part_user:
                p = c.campus_partner_id
            # get all the project names base on the campus partner id
            proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
            for f in proj_camp:
                k = list(Project.objects.filter(id=f.project_name_id))
                for x in k:
                    projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                    sub = list(ProjectSubCategory.objects.filter(project_name_id=x.id))
                    cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                    proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                    for proj_camp_par in proj_camp_par:
                        camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                        camp_part_names.append(camp_part)
                    list_camp_part_names = camp_part_names
                    camp_part_names = []
                    data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                            'activityType': x.activity_type, 'academic_year': x.academic_year,
                            'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                            'description': x.description,
                            'startDate': x.start_date,
                            'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                            'total_uno_hours': x.total_uno_hours,
                            'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                            'total_uno_faculty': x.total_uno_faculty,
                            'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                            'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp, 'sub':sub,
                            'camp_part': list_camp_part_names
                            }
                    projects_list.append(data)
            return render(request, 'projects/projectadd_done.html', {'project': projects_list})
    else:
        project = ProjectFormAdd()
        course = CourseForm()
        formset = mission_details(queryset=ProjectMission.objects.none(), prefix='mission')
        formset4 = secondary_mission_details(queryset=ProjectMission.objects.none(), prefix='secondary_mission')
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none(), prefix='community')
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none(), prefix='campus')
    return render(request, 'projects/projectadd.html',
                  {'project': project, 'formset': formset, 'formset3': formset3, 'course': course,'data_definition':data_definition,
                   'formset2': formset2, 'formset4': formset4})
###my drafts
@login_required()
def myDrafts(request):
    projects_list=[]
    data_definition=DataDefinition.objects.all()
    created_by_user= request.user.email
    created_by= home.models.User.objects.filter(email=created_by_user)
    project_created = Project.objects.filter(created_by__in= created_by)
    project_created_by = [p.id for p in project_created]
    project_updated = Project.objects.filter(updated_by__in=created_by)
    project_updated_by = [p.id for p in project_updated]
    camp_part_user = CampusPartnerUser.objects.filter(user_id = request.user.id)
    camp_part_id = camp_part_user.values_list('campus_partner_id', flat=True)
    proj_camp = ProjectCampusPartner.objects.filter(campus_partner__in=camp_part_id)
    project_ids = [project.project_name_id for project in proj_camp]
    ids = list(set(project_ids).union(project_created_by).union(project_updated_by))
    if request.user.is_superuser == True:
        ids = [project.id for project in Project.objects.all()]
    cursor = connection.cursor()
    cursor.execute(sql.my_drafts, [ids])
    for obj in cursor.fetchall():
        projects_list.append(
            {"name": obj[0].split("(")[0], "projmisn": obj[1], "comm_part": obj[2], "camp_part": obj[3],
             "engagementType": obj[4], "academic_year": obj[5],
             "semester": obj[6], "status": obj[7], "startDate": obj[8], "endDate": obj[9], "outcomes": obj[10],
             "total_uno_students": obj[11],
             "total_uno_hours": obj[12], "total_uno_faculty": obj[13], "total_k12_students": obj[14],
             "total_k12_hours": obj[15],
             "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18],
             "project_type": obj[20], "pk":obj[19]
                , "end_semester": obj[21], "end_academic_year": obj[22], "sub_category": obj[23],
             "campus_lead_staff": obj[24],
             "mission_image": obj[25], "other_activity_type": obj[26], "other_sub_category":obj[27]})

    return render(request, 'projects/myDrafts.html', {'project': projects_list, 'data_definition':data_definition})

@login_required()
def drafts_delete(request,pk):
    draft_delete = get_object_or_404(Project, pk=pk)
    draft_delete.delete()
    return HttpResponseRedirect("/myDrafts")
