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
gmaps = googlemaps.Client(key='AIzaSyBH5afRK4l9rr_HOR_oGJ5Dsiw2ldUzLv0')


@login_required()
@communitypartner_required()
def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)

#    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome,'usertype':usertype})


@login_required()
@communitypartner_required()
def communitypartnerproject(request):
    p = 0
    projects_list=[]
    comm_part_names=[]
    data_definition=DataDefinition.objects.all()
    # Get the campus partner id related to the user
    comm_part_user = CommunityPartnerUser.objects.filter(user_id = request.user.id)
    for c in comm_part_user:
        p =c.community_partner_id
    # get all the project names base on the campus partner id
        proj_comm = list(ProjectCommunityPartner.objects.filter(community_partner_id = p))
        for f in proj_comm:

            k=list(Project.objects.filter(id = f.project_name_id))

            for x in k:
             projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
             cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))

             camp = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
             proj_comm_par = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
             for proj_comm_par in proj_comm_par:
                comm_part = CommunityPartner.objects.get(id=proj_comm_par.community_partner_id)

                comm_part_names.append(comm_part)
             list_comm_part_names = comm_part_names

             comm_part_names = []
         #total_project_hours += proj_cam_par.total_hours

             data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                'activityType': x.activity_type,
                'facilitator': x.facilitator, 'semester': x.semester , 'status': x.status,
                'startDate': x.start_date,
                'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                'total_uno_hours': x.total_uno_hours,
                'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                'total_uno_faculty': x.total_uno_faculty,
                'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                'total_economic_impact': x.total_economic_impact,'description':x.description,'projmisn': projmisn, 'proj_comm': proj_comm,
                'camp':camp, 'comm_part':list_comm_part_names
                 }

             projects_list.append(data)



    return render(request, 'projects/community_partner_projects.html', {'project': projects_list,'data_definition':data_definition})


@login_required()
# @campuspartner_required()
def proj_view_user(request):

    projects_list=[]
    data_definition=DataDefinition.objects.all()
    camp_part_names=[]
    # Get the campus partner id's related to the user
    camp_part_user = CampusPartnerUser.objects.filter(user_id = request.user.id)
    for c in camp_part_user:
        p = c.campus_partner_id
        # get all the project names base on the campus partner id
        proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id = p))

        for f in proj_camp:

            k=list(Project.objects.filter(id = f.project_name_id))

            for x in k:
             projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
             cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
             proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
             for proj_camp_par in proj_camp_par:
                camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)

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
                'total_economic_impact': x.total_economic_impact,'projmisn': projmisn, 'cp': cp, 'camp_part':list_camp_part_names
                 }

             projects_list.append(data)



    return render(request, 'projects/Projectlist.html', {'project': projects_list,'data_definition':data_definition})


@login_required()
# @campuspartner_required()

def project_total_Add(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    secondary_mission_details = modelformset_factory(ProjectMission, extra=1, form=ScndProjectMissionFormset)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition=DataDefinition.objects.all()
    if request.method == 'POST':
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None, prefix='mission')
        formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid() and formset3.is_valid() and formset4.is_valid():
            ##Convert address to cordinates and save the legislatve district and household income
            a = 0
            project.total_uno_hours = a
            proj = project.save()
            proj.project_name = proj.project_name + " :" + str(proj.academic_year)
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
                    formset4 = secondary_mission_details(queryset=ProjectMission.objects.none())
                    # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
                    formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
                    return render(request, 'projects/projectadd.html',
                                  {'project': project, 'formset': formset, 'formset4': formset4,'formset3': formset3, 'course': course})
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
            secondary_mission_form = formset4.save(commit=False)
            proj_comm_form = formset2.save(commit=False)
            proj_campus_form = formset3.save(commit=False)
            for k in proj_comm_form:
                k.project_name = proj

                k.save()

            for form in mission_form:
                form.project_name = proj

                form.mission_type = 'Primary'
                form.save()


            for form4 in secondary_mission_form:
                form4.project_name = proj

                form4.mission_type = 'Other'
                form4.save()

            # projh = Project.objects.get(pk=project_name_id.pk)
            init = 0
            t = 0
            for c in proj_campus_form:
                c.project_name = proj
                c.save()
                # init = proj.total_uno_hours
                t += c.total_hours * c.total_people

                proj.total_uno_hours = t
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
            return render(request, 'projects/projectadd_done.html', {'project': projects_list})
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
        formset4 = secondary_mission_details(queryset=ProjectMission.objects.none(), prefix='secondary_mission')
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none(), prefix='community')
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none(), prefix='campus')

    return render(request, 'projects/projectadd.html',
                  {'project': project, 'formset': formset, 'formset3': formset3, 'course': course,'data_definition':data_definition,
                   'formset2': formset2, 'formset4': formset4})

@login_required()
@campuspartner_required()
def project_edit_new(request,pk):

    mission_edit_details = inlineformset_factory(Project,ProjectMission, extra=0,min_num=1,can_delete=True, form=ProjectMissionEditFormset)
    proj_comm_part_edit = inlineformset_factory(Project,ProjectCommunityPartner, extra=0,min_num=1, can_delete=True, form=AddProjectCommunityPartnerForm)
    proj_campus_part_edit = inlineformset_factory(Project,ProjectCampusPartner, extra=0,min_num=1, can_delete=True,  form=AddProjectCampusPartnerForm)
    #print('print input to edit')

    if request.method == 'POST':
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
                            tot_hours += proj_camp_par.total_hours * proj_camp_par.total_people
                            # total_project_hours += proj_camp_par.total_hours
                            x.total_uno_hours = tot_hours
                            x.total_uno_students += proj_camp_par.total_people
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

                return HttpResponseRedirect("/campususerproject")
                #return render(request, 'projects/Projectlist.html', {'project': projects_list})

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
            return render(request,'projects/projectedit.html',{'project': project,'course': course,
                                                   'formset_missiondetails':formset_missiondetails,
                                                   'formset_comm_details': formset_comm_details,
                                                   'formset_camp_details':formset_camp_details})

@login_required()
@login_required()
def SearchForProject(request):

    data_definition=DataDefinition.objects.all()

    projects_list = []

    if request.method == "GET":

        # To get list of all Projects frm the Database
        projects = list(Project.objects.all())

        for x in projects:

            # Finding the Mission of each project from ProjectMission Table
            projmisn =ProjectMission.objects.filter(project_name_id=x.id).values('mission__mission_name','mission_type')

            # Finding the Community Partner of each Project from ProjectCommunityPartner Table
            proj_comm_par = ProjectCommunityPartner.objects.filter(project_name_id=x.id).values_list('community_partner__name', flat=True)

            # Finding the Campus Partner of each Project from ProjectCampusPartner Table
            proj_camp_par = ProjectCampusPartner.objects.filter(project_name_id=x.id).values_list('campus_partner__name',flat=True)

            data = {'pk': x.pk, 'name': x.project_name.split(":")[0], 'engagementType': x.engagement_type,'academic_year' : x.academic_year,
                    'activityType': x.activity_type,
                    'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                    'description': x.description,
                    'startDate': x.start_date,
                    'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                    'total_uno_hours': x.total_uno_hours,
                    'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                    'total_uno_faculty': x.total_uno_faculty,
                    'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                    'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'comm_part': proj_comm_par,
                    'camp_part': proj_camp_par
                    }
            projects_list.append(data)

    return render(request,'projects/SearchProject.html',{'project': projects_list, 'data_definition':data_definition})


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
    return redirect("proj_view_user")


# List Projects for Public View

def projectsPublicReport(request):
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    data_definition = DataDefinition.objects.all()
    projectsData = []
    camp_part = []
    comm_part = []
    for project in projects.qs:
        projectMissions = ProjectMission.objects.filter(project_name_id=project, mission_type='Primary')
        data = {}
        for mission in projectMissions:
            if mission in missions.qs:
                projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                for projectCampusPartner in projectCampusPartners:
                    if projectCampusPartner.campus_partner in campusPartners.qs:

                        a = ProjectCommunityPartner.objects.all().values_list('project_name', flat=True)
                        if project.id not in a:
                            b = request.GET.get('community_type', None)
                            c = request.GET.get('weitz_cec_part', None)
                            if b is None or b == "All" or b == '':
                                if c is None or c == "All" or c == '':
                                    data['projectName'] = project.project_name
                                    data['engagementType'] = project.engagement_type

                                    projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                                    for projectCampusPartner in projectCampusPartners:
                                        camp_part.append(projectCampusPartner.campus_partner)
                                    list_camp = camp_part
                                    camp_part = []
                                    data['campusPartner'] = list_camp

                        projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
                        for projectCommunityPartner in projectCommunityPartners:
                            if projectCommunityPartner.community_partner in communityPartners.qs:
                                data['projectName'] = project.project_name.split(":")[0]
                                data['engagementType'] = project.engagement_type

                                projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                                for projectCampusPartner in projectCampusPartners:
                                    camp_part.append(projectCampusPartner.campus_partner)
                                list_camp = camp_part
                                camp_part = []
                                data['campusPartner'] = list_camp

                                projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
                                for projectCommunityPartner in projectCommunityPartners:
                                    comm_part.append(projectCommunityPartner.community_partner)
                                list_comm = comm_part
                                comm_part = []
                                data['communityPartner'] = list_comm
        if data:
            projectsData.append(data)

    return render(request, 'reports/projects_public_view.html', {'projects': projects,'data_definition':data_definition,
                  'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners, "campusPartners":campusPartners})


# List of community Partners Public View (Vineeth version)

def communityPublicReport(request):
    community_dict = {}
    community_list = []
    data_definition=DataDefinition.objects.all()
    proj_comm = ProjectCommunityFilter(request.GET,queryset=ProjectCommunityPartner.objects.all())
    proj_comm_ids = [comm.community_partner_id for comm in proj_comm.qs]
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    # communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(id__in=proj_comm_ids)) #To get community partners that have atleast one project
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())   # This filters project mission areas not community partners mission areas
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())


    for m in communityPartners.qs:
        campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
        campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
        campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]

        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

        missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
        mission_filtered_ids = [mission.project_name_id for mission in missions.qs]

        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]

        proj_ids = list(set(campus_project_filtered_ids).intersection(campus_filtered_ids))
        proj_ids1 = list(set(proj_ids).intersection(mission_filtered_ids))
        project_ids = list(set(proj_ids1).intersection(project_filtered_ids))

        community_dict['community_name'] = m.name
        project_count = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).filter(project_name_id__in=project_ids).count()
        community_dict['project_count'] = project_count
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        community_list.append(community_dict.copy())

    return render(request, 'reports/community_public_view.html', { 'college_filter': campus_partner_filter, 'campus_filter': campus_filter,
                                                                'project_filter': project_filter,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 'missions': missions,
                                                                 'data_definition':data_definition})


# List Projects for Private View
@admin_required()
def projectsPrivateReport(request):
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    data_definition=DataDefinition.objects.all()
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    projectsData = []
    camp_part = []
    comm_part = []
    for project in projects.qs:
        projectMissions = ProjectMission.objects.filter(project_name_id=project.id, mission_type='Primary')
        data = {}
        for mission in projectMissions:
            if mission in missions.qs:
                projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                for projectCampusPartner in projectCampusPartners:
                    if projectCampusPartner.campus_partner in campusPartners.qs:

                        a = ProjectCommunityPartner.objects.all().values_list('project_name', flat=True)
                        if project.id not in a:
                            b = request.GET.get('community_type', None)
                            c = request.GET.get('weitz_cec_part', None)
                            if b is None or b == "All" or b == '':
                                if c is None or c == "All" or c == '':
                                    data['projectName'] = mission.project_name
                                    data['engagementType'] = project.engagement_type
                                    data['total_UNO_students'] = project.total_uno_students
                                    data['total_hours'] = project.total_uno_hours
                                    data['economic_impact'] = project.total_economic_impact

                                    projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                                    for projectCampusPartner in projectCampusPartners:
                                        camp_part.append(projectCampusPartner.campus_partner)
                                    list_camp = camp_part
                                    camp_part = []
                                    data['campusPartner'] = list_camp

                        projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
                        for projectCommunityPartner in projectCommunityPartners:
                            if projectCommunityPartner.community_partner in communityPartners.qs:
                                data['projectName'] = project.project_name.split(":")[0]
                                data['engagementType'] = project.engagement_type
                                data['total_UNO_students'] = project.total_uno_students
                                data['total_hours'] = project.total_uno_hours
                                data['economic_impact'] = project.total_economic_impact

                                projectCampusPartners = ProjectCampusPartner.objects.filter(project_name_id=project.id)
                                for projectCampusPartner in projectCampusPartners:
                                    camp_part.append(projectCampusPartner.campus_partner)
                                list_camp = camp_part
                                camp_part = []
                                data['campusPartner'] = list_camp

                                projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name_id=project.id)
                                for projectCommunityPartner in projectCommunityPartners:
                                    comm_part.append(projectCommunityPartner.community_partner)
                                list_comm = comm_part
                                comm_part = []
                                data['communityPartner'] = list_comm
        if data:
            projectsData.append(data)

    return render(request, 'reports/projects_private_view.html', {'projects': projects,'data_definition':data_definition,
                  'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners, "campusPartners":campusPartners})


@login_required()
def communityPrivateReport(request):
    community_dict = {}
    community_list = []
    comp_part_contact = []
    data_definition=DataDefinition.objects.all()
    proj_comm = ProjectCommunityFilter(request.GET, queryset=ProjectCommunityPartner.objects.all())
    proj_comm_ids = [comm.community_partner_id for comm in proj_comm.qs]
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.filter(id__in=proj_comm_ids))
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())   # This filters project mission areas not community partners mission areas
    campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
    campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())

    for m in communityPartners.qs:
        campus_partner_filter = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
        campus_partner_filtered_ids = [campus.id for campus in campus_partner_filter.qs]
        campus_project_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.filter(campus_partner_id__in=campus_partner_filtered_ids))
        campus_project_filtered_ids = [project.project_name_id for project in campus_project_filter.qs]

        campus_filter = ProjectCampusFilter(request.GET, queryset=ProjectCampusPartner.objects.all())
        campus_filtered_ids = [project.project_name_id for project in campus_filter.qs]

        missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.filter(mission_type='Primary'))
        mission_filtered_ids = [mission.project_name_id for mission in missions.qs]

        project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
        project_filtered_ids = [project.id for project in project_filter.qs]

        proj_ids = list(set(campus_project_filtered_ids).intersection(campus_filtered_ids))
        proj_ids1 = list(set(proj_ids).intersection(mission_filtered_ids))
        project_ids = list(set(proj_ids1).intersection(project_filtered_ids))

        community_dict['community_name'] = m.name
        community_dict['website'] = m.website_url
        project_count = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).filter(project_name_id__in=project_ids).count()
        community_dict['project_count'] = project_count

        # Code to get the contact email id of community partners from Contacts Model
        contact = list(Contact.objects.filter(community_partner=m.id, contact_type='Primary'))
        for contact in contact:
            comp_part_contact.append(contact.email_id)
        list_contacts = comp_part_contact
        comp_part_contact = []
        community_dict['email'] = list_contacts

        # Code to get the uno hours, students, economic impact form Project Table
        total_uno_students = 0
        total_uno_hours = 0
        total_economic_impact= 0
        p_community = ProjectCommunityPartner.objects.filter(community_partner_id=m.id).filter(project_name_id__in=project_ids)
        for pm in p_community:
            uno_students = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_students'))
            uno_hours = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_uno_hours'))
            economic_impact = Project.objects.filter(id=pm.project_name_id).aggregate(Sum('total_economic_impact'))
            total_uno_students += uno_students['total_uno_students__sum']
            total_uno_hours += uno_hours['total_uno_hours__sum']
            total_economic_impact += economic_impact['total_economic_impact__sum']
        community_dict['total_uno_hours'] = total_uno_hours
        community_dict['total_uno_students'] = total_uno_students
        community_dict['total_economic_impact'] = total_economic_impact
        communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
        community_list.append(community_dict.copy())

    return render(request, 'reports/community_private_view.html', {'college_filter': campus_partner_filter,'project_filter': project_filter,'data_definition':data_definition,
                                                                 'communityPartners': communityPartners,
                                                                 'community_list': community_list,
                                                                 'missions': missions, 'campus_filter': campus_filter})

# commented old code (community, projects public and private reports

# List of community Partners Public View
# def communityPublicReport(request):
#
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     projects = ProjectFilter(request.GET, queryset=Project.objects.all())
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
#     communityData = []
#
#     for partner in communityPartners.qs:
#         data={}
#         data["name"] = partner.name
#         communityProjects = ProjectCommunityPartner.objects.filter(community_partner=partner.id)
#         count = 0
#         for cproject in communityProjects:
#             project = cproject.project_name
#             projectMissions = ProjectMission.objects.filter(project_name=project)
#             if project in projects.qs:
#                 count +=1
#             for mission in projectMissions:
#                 if mission in missions.qs and count == 0:
#                     count +=1
#         data['communityProjects'] = count
#         communityData.append(data)
#
#
#     return render(request, 'reports/community_public_view.html',
#                    {'communityPartners': communityPartners, "projects": projects,
#                     'communityData': communityData, 'missions': missions})

# List of community Partners Private View
# @login_required()
# def communityPrivateReport(request):
#
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     projects = ProjectFilter(request.GET, queryset=Project.objects.all())
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
#     communityData = []
#
#     for partner in communityPartners.qs:
#         data={}
#         data["name"] = partner.name
#         data['website'] = partner.website_url
#         try:
#             contact = Contact.objects.get(community_partner=partner, contact_type='Primary')
#         except Contact.DoesNotExist:
#             contact = None
#
#         if contact:
#             data['email'] = contact.email_id
#         else:
#             data['email'] = "Email Not Provided"
#
#         communityProjects = ProjectCommunityPartner.objects.filter(community_partner=partner.id)
#         count = 0
#         for cproject in communityProjects:
#             project = cproject.project_name
#             projectMissions = ProjectMission.objects.filter(project_name=project)
#             if project in projects.qs:
#                 count += 1 #project = Project.objects.  get(id=cproject.id)
#                 if "total_hours" in data:
#                     data['total_UNO_students'] = data['total_UNO_students'] + project.total_uno_students
#                     data['total_hours'] = data['total_hours'] + project.total_uno_hours
#                     data['economic_impact'] = data['economic_impact'] + project.total_economic_impact
#                 else:
#                     data['total_UNO_students'] = project.total_uno_students
#                     data['total_hours'] = project.total_uno_hours
#                     data['economic_impact'] = project.total_economic_impact
#                 count +=1
#             for mission in projectMissions:
#                 if mission in missions.qs and count == 0:
#                     count +=1
#         data['communityProjects'] = count
#         communityData.append(data)
#
#     return render(request, 'reports/community_private_view.html',
#                    {'communityPartners': communityPartners, "projects": projects,
#                     'communityData': communityData, 'missions': missions})

# List Projects for Public View
# def projectsPublicReport(request):
#     projects = ProjectFilter(request.GET, queryset=Project.objects.all())
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     projectsData = []
#     for project in projects.qs:
#         projectMissions = ProjectMission.objects.filter(project_name=project)
#         data = {}
#         for mission in projectMissions:
#             if mission in missions.qs:
#                 data['projectName'] = project.project_name
#                 data['engagementType'] = project.engagement_type
#
#                 try:
#                     projectCampusPartners = ProjectCampusPartner.objects.filter(project_name=project.id)
#                     for projectCampusPartner in projectCampusPartners:
#                         if "campusPartner" in data:
#                             data['campusPartner'] = data[
#                                 'campusPartner']  # + ", " + str(projectCampusPartner.campus_partner)
#                         else:
#                             data['campusPartner'] = projectCampusPartner.campus_partner
#                 except ProjectCampusPartner.DoesNotExist:
#                     data['campusPartner'] = None
#
#                 if data['campusPartner']:
#                     try:
#                         projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name=project.id)
#                         for projectCommunityPartner in projectCommunityPartners:
#                             if projectCommunityPartner.community_partner in communityPartners.qs:
#                                 if "communityPartner" in data:
#                                     data['communityPartner'] = data[
#                                         'communityPartner']  # + ", " + str(projectCommunityPartner.community_partner)
#                                 else:
#                                     data['communityPartner'] = projectCommunityPartner.community_partner
#                     except ProjectCommunityPartner.DoesNotExist:
#                         data['communityPartner'] = ""
#                 break
#
#         if data:
#             projectsData.append(data)
#
#     return render(request, 'reports/projects_public_view.html', {'projects': projects,
#                                                                  'projectsData': projectsData, "missions": missions,
#                                                                  "communityPartners": communityPartners})

# List Projects for Private View
# @login_required()
# def projectsPrivateReport(request):
#
#     projects = ProjectFilter(request.GET, queryset=Project.objects.all())
#     missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
#     communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
#     projectsData = []
#     for project in projects.qs:
#         projectMissions = ProjectMission.objects.filter(project_name=project)
#         data = {}
#         for mission in projectMissions:
#             if mission in missions.qs:
#                 data['projectName'] = project.project_name
#                 data['engagementType'] = project.engagement_type
#                 data['total_UNO_students'] = project.total_uno_students
#                 data['total_hours'] = project.total_uno_hours
#                 data['economic_impact'] = project.total_economic_impact
#
#                 try:
#                     projectCampusPartners = ProjectCampusPartner.objects.filter(project_name=project.id)
#                     for projectCampusPartner in projectCampusPartners:
#                         if "campusPartner" in data:
#                             data['campusPartner'] = data['campusPartner'] #+ ", " + str(projectCampusPartner.campus_partner)
#                         else:
#                             data['campusPartner'] = projectCampusPartner.campus_partner
#                 except ProjectCampusPartner.DoesNotExist:
#                     data['campusPartner'] = None
#
#                 if data['campusPartner']:
#                     try:
#                         projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name=project.id)
#                         for projectCommunityPartner in projectCommunityPartners:
#                             if projectCommunityPartner.community_partner in communityPartners.qs:
#                                 if "communityPartner" in data:
#                                     data['communityPartner'] = data['communityPartner'] #+ ", " + str(projectCommunityPartner.community_partner)
#                                 else:
#                                     data['communityPartner'] = projectCommunityPartner.community_partner
#                     except ProjectCommunityPartner.DoesNotExist:
#                         data['communityPartner'] = ""
#                 break
#
#         if data:
#             projectsData.append(data)
#
#
#     return render(request, 'reports/projects_private_view.html', {'projects': projects,
#                   'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners})
