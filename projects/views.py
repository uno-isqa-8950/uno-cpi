from decimal import *
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from numpy import shape
from home.decorators import communitypartner_required, campuspartner_required, admin_required
from home.views import gmaps
from partners.views import district, countyData
from projects.models import *
from home.models import *
from home.filters import *
from partners.models import *
from university.models import Course
from .forms import ProjectCommunityPartnerForm, CourseForm, ProjectFormAdd
from django.contrib.auth.decorators import login_required
from .models import Project,ProjectMission, ProjectCommunityPartner, ProjectCampusPartner, Status ,EngagementType, ActivityType
from .forms import ProjectForm, ProjectMissionForm, ScndProjectMissionFormset
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
    # Get the campus partner id's related to the user
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
             "total_k12_hours": obj[15], "pk":obj[19],
             "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18]})

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


@login_required()
def createProject(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    #secondary_mission_details = modelformset_factory(ProjectMission, extra=1, form=ScndProjectMissionFormset)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition=DataDefinition.objects.all()
    if request.method == 'POST':
        # cache.clear()
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None, prefix='mission')
        #formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid() and formset3.is_valid():
            ##Convert address to cordinates and save the legislatve district and household income
            #a = 0
            #project.total_uno_hours = a
            proj = project.save()
            proj.project_name = proj.project_name + ": " + str(proj.academic_year) + " (" + str(proj.id) + ")"
            eng = str(proj.engagement_type)

            address = proj.address_line1
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
                    #formset4 = secondary_mission_details(queryset=ProjectMission.objects.none())
                    # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
                    formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
                    return render(request, 'projects/createProject.html',
                                  {'project': project, 'formset': formset,'formset3': formset3, 'course': course})
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
            #secondary_mission_form = formset4.save(commit=False)
            proj_comm_form = formset2.save(commit=False)
            proj_campus_form = formset3.save(commit=False)
            for k in proj_comm_form:
                k.project_name = proj

                k.save()

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
                #t += c.total_hours * c.total_people

                #proj.total_uno_hours = t
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
                            'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp,
                            'camp_part': list_camp_part_names
                            }
                    projects_list.append(data)
            return render(request, 'projects/confirmAddProject.html', {'project': projects_list})
    else:
        month=datetime.datetime.now() .month
        year=datetime.datetime.now() .year
        if month > 7:
            a_year =str(year)+"-"+str(year+1) [-2:]
        else:
            a_year = str(year-1) + "-" + str(year) [-2:]

        test = AcademicYear.objects.get(academic_year=a_year)
        project =ProjectFormAdd(initial={"academic_year":test})
        course = CourseForm()
        formset = mission_details(queryset=ProjectMission.objects.none(), prefix='mission')
        #formset4 = secondary_mission_details(queryset=ProjectMission.objects.none(), prefix='secondary_mission')
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none(), prefix='community')
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none(), prefix='campus')

    return render(request, 'projects/createProject.html',
                  {'project': project, 'formset': formset, 'formset3': formset3, 'course': course,'data_definition':data_definition,
                   'formset2': formset2})

@login_required()
def editProject(request,pk):

    mission_edit_details = inlineformset_factory(Project,ProjectMission, extra=0,min_num=1,can_delete=True, form=ProjectMissionEditFormset)
    proj_comm_part_edit = inlineformset_factory(Project,ProjectCommunityPartner, extra=0,min_num=1, can_delete=True, form=AddProjectCommunityPartnerForm)
    proj_campus_part_edit = inlineformset_factory(Project,ProjectCampusPartner, extra=0,min_num=1, can_delete=True,  form=AddProjectCampusPartnerForm)
    #print('print input to edit')

    if request.method == 'POST':
        # cache.clear()
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)
            course = CourseForm(request.POST or None, instance=x)

        formset_missiondetails = mission_edit_details(request.POST, request.FILES, instance=x, prefix='mission_edit')
        formset_comm_details = proj_comm_part_edit(request.POST, request.FILES, instance=x, prefix='community_edit')
        formset_camp_details = proj_campus_part_edit(request.POST, request.FILES, instance=x, prefix='campus_edit')
        if project.is_valid() and formset_camp_details.is_valid() and formset_comm_details.is_valid() and formset_missiondetails.is_valid():

                instances = project.save()
                pm = formset_missiondetails.save()
                compar= formset_comm_details.save()
                campar= formset_camp_details.save()

                for k in pm:
                    k.project_name = instances
                    k.save()
                for p in compar:
                    p.project_name= instances
                    p.save()
                for l in campar:
                    l.project_name= instances
                    l.save()
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

                        projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                        cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                        proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
                        for proj_camp_par in proj_camp_par:
                            camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
                            #tot_hours += proj_camp_par.total_hours * proj_camp_par.total_people
                            # total_project_hours += proj_camp_par.total_hours
                            #x.total_uno_hours = tot_hours
                            #x.total_uno_students += proj_camp_par.total_people
                            x.save()
                            camp_part_names.append(camp_part)
                        list_camp_part_names = camp_part_names
                        camp_part_names = []

                        data = {'pk': x.pk, 'name': x.project_name.split(":")[0], 'engagementType': x.engagement_type,
                                'activityType': x.activity_type, 'academic_year': x.academic_year,
                                'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,'description':x.description,
                                'startDate': x.start_date,
                                'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                                'total_uno_hours': x.total_uno_hours,
                                'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                                'total_uno_faculty': x.total_uno_faculty,
                                'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                                'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp,
                                'camp_part': list_camp_part_names,
                                }

                        projects_list.append(data)

                return HttpResponseRedirect("/myProjects")
                #return render(request, 'projects/myProjects.html', {'project': projects_list})

    else:

            proj_edit = Project.objects.filter(id=pk)

            for x in proj_edit:
                project = ProjectForm2(request.POST or None, instance=x)
            course = CourseForm(instance = x)

            proj_mission = ProjectMission.objects.filter(project_name_id=pk)
            proj_comm_part = ProjectCommunityPartner.objects.filter(project_name_id = pk)
            proj_camp_part = ProjectCampusPartner.objects.filter(project_name_id = pk)
            # course_details = course(instance= x)
            formset_missiondetails = mission_edit_details(instance=x, prefix='mission_edit')
            formset_comm_details = proj_comm_part_edit(instance=x, prefix='community_edit')
            formset_camp_details = proj_campus_part_edit(instance=x, prefix='campus_edit')
            return render(request, 'projects/editProject.html', {'project': project, 'course': course,
                                                   'formset_missiondetails':formset_missiondetails,
                                                   'formset_comm_details': formset_comm_details,
                                                   'formset_camp_details':formset_camp_details})


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


@login_required()
def showAllProjects(request):
    data_definition=DataDefinition.objects.all()
    projects_list=[]
    cursor = connection.cursor()
    cursor.execute(sql.all_projects_sql)
    for obj in cursor.fetchall():
         projects_list.append({"name": obj[0].split("(")[0], "projmisn": obj[1],"comm_part": obj[2], "camp_part": obj[3],"engagementType": obj[4], "academic_year": obj[5],
                              "semester": obj[6], "status": obj[7],"startDate": obj[8], "endDate": obj[9],"outcomes": obj[10], "total_uno_students": obj[11],
                              "total_uno_hours": obj[12], "total_uno_faculty": obj[13],"total_k12_students": obj[14], "total_k12_hours": obj[15],
                              "total_other_community_members": obj[16], "activityType": obj[17], "description": obj[18]})
    return render(request, 'projects/allProjects.html', {'project': projects_list, 'data_definition':data_definition})





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


# List Projects for Public View

# def projectsPublicReport(request):
#     projects = ProjectFilter(request.GET, queryset=Project.objects.all())
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
#     data_definition = DataDefinition.objects.all()
#     projectsData = []
#     camp_part = []
#     comm_part = []
#     for project in projects.qs:
#         projectMissions = ProjectMission.objects.filter(project_name_id=project, mission_type='Primary')
#         data = {}
#         for mission in projectMissions:
#             if mission in missions.qs:
#                 projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
#                 for projectCampusPartner in projectCampusPartners:
#                     if projectCampusPartner.campus_partner in campusPartners.qs:
#
#                         a = ProjectCommunityPartner.objects.all().values_list('project_name', flat=True)
#                         if project.id not in a:
#                             b = request.GET.get('community_type', None)
#                             c = request.GET.get('weitz_cec_part', None)
#                             if b is None or b == "All" or b == '':
#                                 if c is None or c == "All" or c == '':
#                                     data['projectName'] = project.project_name
#                                     data['engagementType'] = project.engagement_type
#
#                                     projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
#                                     for projectCampusPartner in projectCampusPartners:
#                                         camp_part.append(projectCampusPartner.campus_partner)
#                                     list_camp = camp_part
#                                     camp_part = []
#                                     data['campusPartner'] = list_camp
#
#                         projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
#                         for projectCommunityPartner in projectCommunityPartners:
#                             if projectCommunityPartner.community_partner in communityPartners.qs:
#                                 data['projectName'] = project.project_name.split("(")[0]
#                                 data['engagementType'] = project.engagement_type
#
#                                 projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
#                                 for projectCampusPartner in projectCampusPartners:
#                                     camp_part.append(projectCampusPartner.campus_partner)
#                                 list_camp = camp_part
#                                 camp_part = []
#                                 data['campusPartner'] = list_camp
#
#                                 projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
#                                 for projectCommunityPartner in projectCommunityPartners:
#                                     comm_part.append(projectCommunityPartner.community_partner)
#                                 list_comm = comm_part
#                                 comm_part = []
#                                 data['communityPartner'] = list_comm
#         if data:
#             projectsData.append(data)
#
#     return render(request, 'reports/projects_public_view.html', {'projects': projects,'data_definition':data_definition,
#                   'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners, "campusPartners":campusPartners})

# Projects Report Speed up Version (Vineeth)

def projectsPublicReport(request):
    # data= {}
    data_list=[]
    data_definition = DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

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

    cursor = connection.cursor()
    cursor.execute(sql.projects_report, [project_ids])

    for obj in cursor.fetchall():
        data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                          "engagementType": obj[3]})

    b = request.GET.get('community_type', None)
    c = request.GET.get('weitz_cec_part', None)
    if b is None or b == "All" or b == '':
        if c is None or c == "All" or c == '':
            cursor.execute(sql.projects_report, [projects_comm_ids])

            for obj in cursor.fetchall():
                data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                     "engagementType": obj[3]})

    # for project in projects:
    #     data['projectName']= project.project_name
    #     data['engagementType']=project.engagement_type
    #     # Finding the Community Partner of each Project from ProjectCommunityPartner Table
    #     proj_comm_par = ProjectCommunityPartner.objects.filter(project_name_id=project.id).values_list('community_partner__name', flat=True)
    #     # Finding the Campus Partner of each Project from ProjectCampusPartner Table
    #     proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=project.id).values_list('campus_partner__name', flat=True)
    #     data['campusPartner'] = proj_camp_par
    #     data['communityPartner']= proj_comm_par
    #     data_list.append(data.copy())
    #
    # # This Part is to display any Projects without Community Partners
    # for project in projects_comm:
    #     b = request.GET.get('community_type', None)
    #     c = request.GET.get('weitz_cec_part', None)
    #     if b is None or b == "All" or b == '':
    #         if c is None or c == "All" or c == '':
    #             data['projectName'] = project.project_name
    #             data['engagementType'] = project.engagement_type
    #             proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=project.id).values_list('campus_partner__name', flat=True)
    #             data['campusPartner'] = proj_camp_par
    #             data['communityPartner'] = []
    #             data_list.append(data.copy())

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
                   'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
                   "campus_filter": campus_filter, 'college_filter': campusPartners, 'campus_id':campus_id})

# Trying to speed up the project reports (Vineeth)
# List Projects for Private View

@admin_required()
def projectsPrivateReport(request):
    data= {}
    data_list=[]
    data_definition = DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

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
    cursor = connection.cursor()
    cursor.execute(sql.projects_report, [project_ids])

    for obj in cursor.fetchall():
        data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                          "engagementType": obj[3]})

    b = request.GET.get('community_type', None)
    c = request.GET.get('weitz_cec_part', None)
    if b is None or b == "All" or b == '':
        if c is None or c == "All" or c == '':
            cursor.execute(sql.projects_report, [projects_comm_ids])

            for obj in cursor.fetchall():
                data_list.append({"projectName": obj[0].split("(")[0], "communityPartner": obj[1], "campusPartner": obj[2],
                     "engagementType": obj[3]})

    # for project in projects:
    #     data['projectName']= project.project_name
    #     data['engagementType']=project.engagement_type
    #     data['total_UNO_students'] = project.total_uno_students
    #     data['total_hours'] = project.total_uno_hours
    #     data['economic_impact'] = project.total_economic_impact
    #     # Finding the Community Partner of each Project from ProjectCommunityPartner Table
    #     proj_comm_par = ProjectCommunityPartner.objects.filter(project_name_id=project.id).values_list('community_partner__name', flat=True)
    #     # Finding the Campus Partner of each Project from ProjectCampusPartner Table
    #     proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=project.id).values_list('campus_partner__name', flat=True)
    #     data['campusPartner'] = proj_camp_par
    #     data['communityPartner']= proj_comm_par
    #     data_list.append(data.copy())
    #
    # # This Part is to display any Projects without Community Partners
    # for project in projects_comm:
    #     b = request.GET.get('community_type', None)
    #     c = request.GET.get('weitz_cec_part', None)
    #     if b is None or b == "All" or b == '':
    #         if c is None or c == "All" or c == '':
    #             data['projectName'] = project.project_name.split('(')[0]
    #             data['engagementType'] = project.engagement_type
    #             data['total_UNO_students'] = project.total_uno_students
    #             data['total_hours'] = project.total_uno_hours
    #             data['economic_impact'] = project.total_economic_impact
    #             proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=project.id).values_list('campus_partner__name', flat=True)
    #             data['campusPartner'] = proj_camp_par
    #             data['communityPartner'] = []
    #             data_list.append(data.copy())

    return render(request, 'reports/projects_private_view.html',
                  {'projects': project_filter, 'data_definition': data_definition,
                   'projectsData': data_list, "missions": missions, "communityPartners": communityPartners,
                   "campus_filter": campus_project_filter, 'college_filter': campusPartners})


# List of community Partners Public View

def communityPublicReport(request):
    community_dict = {}
    community_list = []
    data_definition=DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    # missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_partner_filtered_ids = campus_partner_filter.qs.values_list('id',flat=True)
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name',flat=True)

    # mission_filtered_ids = missions.qs.values_list('project_name', flat=True)
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)

    # proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    project_ids = list(set(campus_project_filtered_ids).intersection(project_filtered_ids))

    for m in communityPartners.qs:
        proj_comm_par = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).values_list('project_name',flat=True)
        project_count = len(set(project_ids).intersection(proj_comm_par))
        if project_count == 0:
            continue
        community_mission = CommunityPartnerMission.objects.filter(community_partner_id=m.id).filter(mission_type='Primary').values_list('mission_area__mission_name',flat=True)
        community_dict['community_name'] = m.name
        community_dict['community_mission'] = community_mission
        community_dict['project_count'] = project_count
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


    return render(request, 'reports/community_public_view.html', { 'college_filter': campus_partner_filter, 'campus_filter': campus_project_filter,
                                                                'project_filter': project_filter,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 # 'missions': missions,
                                                                 'data_definition':data_definition,
                                                                 'campus_id':campus_id})



@login_required()
def communityPrivateReport(request):
    community_dict = {}
    community_list = []
    # comp_part_contact = []
    data_definition=DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    # missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    campus_partner_filtered_ids = campus_partner_filter.qs.values_list('id', flat=True)
    campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
    campus_project_filtered_ids = campus_project_filter.qs.values_list('project_name', flat=True)

    # mission_filtered_ids = missions.qs.values_list('project_name', flat=True)
    project_filtered_ids = project_filter.qs.values_list('id', flat=True)

    # proj_ids1 = list(set(campus_project_filtered_ids).intersection(mission_filtered_ids))
    project_ids = list(set(campus_project_filtered_ids).intersection(project_filtered_ids))

    for m in communityPartners.qs:
        proj_comm_par = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).values_list('project_name',flat=True)
        project_count = len(set(project_ids).intersection(proj_comm_par))
        if project_count==0:
            continue
        community_mission = CommunityPartnerMission.objects.filter(community_partner_id=m.id).filter(mission_type='Primary').values_list('mission_area__mission_name', flat=True)
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
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 # 'missions': missions,
                                                                   'campus_filter': campus_project_filter, 'campus_id':campus_id})


#project duplication check
def checkProject(request):
    project = ProjectForm()
    projectNames = []
    combinedList =[]

    for object in Project.objects.order_by('project_name'):
        project = object.project_name.split('(')[0]
        for part in ProjectCommunityPartner.objects.filter(project_name__project_name__exact=object.project_name):
            compartner = part.community_partner

            combinedList = [object.project_name.split('(')[0],str(compartner)]
            if combinedList not in projectNames:
                projectNames.append(combinedList)

    if request.method == 'POST':
        project = ProjectForm(request.POST)

    return render(request, 'projects/checkProject.html',
                  {'project': project, 'projectNames':projectNames})

@login_required()
# @campuspartner_required()
def project_total_Add(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    secondary_mission_details = modelformset_factory(ProjectMission, extra=1, form=ScndProjectMissionFormset)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition=DataDefinition.objects.all()
    if request.method == 'POST':
        # cache.clear()
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None, prefix='mission')
        formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        # print("validation ststus:",project.is_valid() , formset.is_valid() ,course.is_valid() , formset2.is_valid())
        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid() and formset3.is_valid() and formset4.is_valid():
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
            proj_campus_form = formset3.save(commit=False)
            for k in proj_comm_form:
                k.project_name = proj
                print("in add comm")
                print(k.project_name)
                print(k.total_hours, k.total_people)
                k.save()

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
                            'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp,
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
