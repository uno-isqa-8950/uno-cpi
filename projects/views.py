from decimal import *
from django.db import connection
from django.http import HttpResponse
from numpy import shape
from home.decorators import communitypartner_required, campuspartner_required
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
from .forms import ProjectForm, ProjectMissionForm
from django.shortcuts import render, redirect, get_object_or_404 , get_list_or_404
from django.utils import timezone
from  .forms import ProjectMissionFormset,AddProjectCommunityPartnerForm, AddProjectCampusPartnerForm,ProjectForm2
from django.forms import inlineformset_factory, modelformset_factory
from .filters import SearchProjectFilter
import googlemaps
from shapely.geometry import shape, Point
import pandas as pd
import json
gmaps = googlemaps.Client(key='AIzaSyBoBkkxBnB7x_GKESVPDLguK0VxSTSxHiI')


@login_required()
@communitypartner_required()
def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)
#    print(usertype.is_communitypartner)
#    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome,'usertype':usertype})


@login_required()
@communitypartner_required()
def communitypartnerproject(request):
    print(request.user.id)
    projects_list=[]
    comm_part_names=[]
    camp_part_names=[]
    total_project_hours = []
    # Get the campus partner id related to the user
    comm_part_user = CommunityPartnerUser.objects.filter(user_id = request.user.id)
    for c in comm_part_user:
        p =c.community_partner_id
        print(c.community_partner_id)
    # get all the project names base on the campus partner id
    proj_comm = list(ProjectCommunityPartner.objects.filter(community_partner_id = p))
    for f in proj_comm:
        print(f)
        k=list(Project.objects.filter(id = f.project_name_id))
        print(k)
        for x in k:
         projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
         cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
         print(cp)
         camp = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
         proj_comm_par = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
         for proj_comm_par in proj_comm_par:
            comm_part = CommunityPartner.objects.get(id=proj_comm_par.community_partner_id)

            comm_part_names.append(comm_part)
         list_comm_part_names = comm_part_names
         print(list_comm_part_names)
         comm_part_names = []
         #total_project_hours += proj_cam_par.total_hours
         #print(total_project_hours)
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



    return render(request, 'projects/community_partner_projects.html', {'project': projects_list})


@login_required()
@communitypartner_required()
def communitypartnerprojectedit(request,pk):

    mission_edit_details = inlineformset_factory(Project, ProjectMission, extra=0, form=ProjectMissionForm)
    proj_comm_part = inlineformset_factory(Project, ProjectCommunityPartner, extra=0, can_delete=False,
                                           form=ProjectCommunityPartnerForm)
    projects_list = []
    comm_part_names = []
    if request.method == 'POST':
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm(request.POST or None, instance=x)

        mission_form = mission_edit_details(request.POST, request.FILES, instance=x)
        comp_proj_form = proj_comm_part(request.POST, request.FILES, instance=x)

        if project.is_valid()  \
                and comp_proj_form.is_valid():

            instances = project.save()
            commpar = comp_proj_form.save(commit=False)

            for p in commpar:
                p.project = instances
                p.save()
            comm_part_user = CommunityPartnerUser.objects.filter(user_id=request.user.id)
            for c in comm_part_user:
                p = c.community_partner_id
                print(c.community_partner_id)
            proj_comm = list(ProjectCommunityPartner.objects.filter(community_partner_id=p))
            print(proj_comm)
            for f in proj_comm:
                print(f)
                k = list(Project.objects.filter(id=f.project_name_id))
                print(k)
                for x in k:
                    projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                    cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                    proj_comm_par = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                    for proj_comm_par in proj_comm_par:
                        comm_part = CommunityPartner.objects.get(id=proj_comm_par.community_partner_id)
                        # print("camp_part is")
                        # print(camp_part)
                        comm_part_names.append(comm_part)
                    list_comm_part_names = comm_part_names
                    comm_part_names = []

                    data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                            'activityType': x.activity_type,
                            'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                            'startDate': x.start_date,
                            'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                            'total_uno_hours': x.total_uno_hours,
                            'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                            'total_uno_faculty': x.total_uno_faculty,
                            'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                            'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp,
                            'camp_part': list_comm_part_names
                            }

                    projects_list.append(data)

            return render(request, 'projects/community_partner_projects.html', {'project': projects_list})


    else:

        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
          project = ProjectForm(request.POST or None, instance=x)
        proj_mission = ProjectMission.objects.filter(project_name_id=pk)
        proj_comm_part_edit = ProjectCommunityPartner.objects.filter(project_name_id=pk)

        comp_proj_form = proj_comm_part(instance=x)

        return render(request, 'projects/community_partner_projects_edit.html', {'project':project,
                                                                                 'comp_proj_form': comp_proj_form})

@login_required()
@campuspartner_required()
def proj_view_user(request):
    #print(request.user.id)
    projects_list=[]
    camp_part_names=[]
    p=0
    # Get the campus partner id related to the user
    camp_part_user = CampusPartnerUser.objects.filter(user_id = request.user.id)
    for c in camp_part_user:
        p =c.campus_partner_id
        #print(c)
    # get all the project names base on the campus partner id
    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id = p))

    for f in proj_camp:
        #print(l)
        k=list(Project.objects.filter(id = f.project_name_id))
        #print(k)
        for x in k:
         projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
         cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
         proj_camp_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
         for proj_camp_par in proj_camp_par:
            camp_part = CampusPartner.objects.get(id=proj_camp_par.campus_partner_id)
            #print("camp_part is")
            #print(camp_part)
            camp_part_names.append(camp_part)
         list_camp_part_names = camp_part_names
         camp_part_names = []

         data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
            'activityType': x.activity_type,
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



    return render(request, 'projects/Projectlist.html', {'project': projects_list})


@login_required()
@campuspartner_required()
def project_total_Add(request):
    #

    mission_details = modelformset_factory(ProjectMission, extra =1 , form = ProjectMissionFormset)
    proj_comm_part= modelformset_factory(ProjectCommunityPartner, extra=1 , form =AddProjectCommunityPartnerForm)
    proj_campus_part=modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)

    if request.method == 'POST':
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None)
        formset2 = proj_comm_part(request.POST or None)
        formset3 = proj_campus_part(request.POST or None)

        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid():
            ##Convert address to cordinates and save the legislatve district and household income
            proj= project.save()
            #user to project

            ##Project name append
            proj.project_name = proj.project_name + " :" + str(proj.academic_year) + " (" + str(proj.id) + ")"
            print(proj.project_name)
            if (proj.engagement_type == "Service Learning"):
                course = course.save(commit=False)
                course.project_name = proj
                course.save()

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
                    # formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
                    formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
                    print('hello')
                    return render(request, 'projects/projectadd.html',
                              {'project': project, 'formset': formset, 'formset3': formset3, 'course': course})


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




            mission_form = formset.save(commit = False)
            proj_comm_form = formset2.save(commit= False)
            proj_campus_form = formset3.save(commit=False)


            for k in proj_comm_form:
               k.project_name = proj
               # print("in add comm")
               print(k.project_name)
               k.save()
            for form in mission_form:
                form.project_name = proj
                # print("in add mission")
                print(form.project_name)
                form.save()
            for c in proj_campus_form:
                c.project_name = proj
                # print("in add campus")
                print(c.project_name)
                c.save()

                project = Project.objects.filter(created_date__lte=timezone.now())
            projects_list = []

            for x in project:
                projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
                camp_part = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))

                data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                        'activityType': x.activity_type,
                        'facilitator': x.facilitator, 'semester': x.semester,'academic_year': x.academic_year, 'status': x.status,'description':x.description,
                        'startDate': x.start_date,
                        'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                        'total_uno_hours': x.total_uno_hours,
                        'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                        'total_uno_faculty': x.total_uno_faculty,
                        'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                        'total_economic_impact': x.total_economic_impact,
                        'projmisn': projmisn, 'camp_part': camp_part}
                projects_list.append(data)
            return render(request, 'projects/Projectlist.html', {'project':projects_list } )

    else:
        project = ProjectFormAdd()
        course =CourseForm()
        formset = mission_details(queryset=ProjectMission.objects.none())
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
        print('hello')
    return render(request,'projects/projectadd.html',{'project': project, 'formset': formset, 'formset3': formset3, 'course': course, 'formset2' : formset2})

@login_required()
@campuspartner_required()
def project_edit_new(request,pk):
    mission_edit_details = inlineformset_factory(Project,ProjectMission, extra=0,can_delete=False, form=ProjectMissionFormset)
    proj_comm_part_edit = inlineformset_factory(Project,ProjectCommunityPartner, extra=0, can_delete=False, form=AddProjectCommunityPartnerForm)
    proj_campus_part_edit = inlineformset_factory(Project,ProjectCampusPartner, extra=0, can_delete=False,  form=AddProjectCampusPartnerForm)
    print('print input to edit')
    if request.method == 'POST':
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)

        course = CourseForm(request.POST or None, instance= x)
        formset_missiondetails = mission_edit_details(request.POST ,request.FILES, instance =x)
        formset_comm_details = proj_comm_part_edit(request.POST, request.FILES, instance=x)
        formset_camp_details = proj_campus_part_edit(request.POST, request.FILES, instance=x)
        print("before form validations", formset_camp_details.is_valid(), formset_comm_details.is_valid(),project.is_valid(), course.is_valid())
        # print("formset_missiondetails.is_valid()8888888888", formset_missiondetails.is_valid())
        if project.is_valid() and formset_camp_details.is_valid() and formset_comm_details.is_valid():
                #print(" validating the forms here")
                instances = project.save()

                if  course.is_valid():
                    course.project_name = instances
                    course.save()
                print(course)
                pm = formset_missiondetails.save(commit=False)
                compar= formset_comm_details.save(commit=False)
                campar= formset_camp_details.save(commit=False)

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
                    # print(c)
                # get all the project names base on the campus partner id
                proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
                for f in proj_camp:
                    k = list(Project.objects.filter(id=f.project_name_id))
                    # print(k)
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
                                'activityType': x.activity_type,
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


                return render(request, 'projects/Projectlist.html', {'project': projects_list})

    else:
            #print(" Project_edit_new else")
            proj_edit = Project.objects.filter(id=pk)

            for x in proj_edit:
                project = ProjectForm2(request.POST or None, instance=x)


            coursedetail = Course.objects.filter(project_name_id=pk)
            course = CourseForm(instance = x)
            # print(course)
            proj_mission = ProjectMission.objects.filter(project_name_id=pk)
            proj_comm_part = ProjectCommunityPartner.objects.filter(project_name_id = pk)
            proj_camp_part = ProjectCampusPartner.objects.filter(project_name_id = pk)
            # course_details = course(instance= x)
            formset_missiondetails = mission_edit_details(instance=x)
            formset_comm_details = proj_comm_part_edit(instance=x)
            formset_camp_details = proj_campus_part_edit(instance=x)
            return render(request,'projects/projectedit.html',{'project': project,'course': course,
                                                   'formset_missiondetails':formset_missiondetails,
                                                   'formset_comm_details': formset_comm_details,
                                                   'formset_camp_details':formset_camp_details})

@login_required()
def SearchForProject(request):
    names=[]
    p=0
    for project in Project.objects.all():
        names.append(project.project_name)
    #print(names)

    camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
    for c in camp_part_user:
        p = c.campus_partner_id
        # print(c)
    # get all the project names base on the campus partner id
    proj_camp = list(ProjectCampusPartner.objects.filter(campus_partner_id=p))
    #print(proj_camp)
    allProjects = SearchProjectFilter(request.GET, queryset=Project.objects.all())
    yesNolist = []
    pnames = []
    cpnames = []

    for project in Project.objects.all():
        pnames.append(project.project_name)
        for checkProject in proj_camp:
            cpnames.append(checkProject.project_name.project_name)

    for project in Project.objects.all():
        if project.project_name in set(cpnames):
            yesNolist.append(False)
        else:
            yesNolist.append(True)


    if request.method == "GET":
        searched_project = SearchProjectFilter(request.GET, queryset=Project.objects.all())
         #@login_required()
        project_ids = [p.id for p in searched_project.qs]
        project_details = Project.objects.filter(id__in=project_ids)
        NameOfProject= [p.project_name for p in searched_project.qs]
        camp_part_user = CampusPartnerUser.objects.filter(user_id=request.user.id)
        # camp_partner = camp_part_user[0].campus_partner
         #
        search_project_filtered = SearchProjectFilter(request.GET)
        #SearchedProjectSave= ProjectCampusPartner( project_name=search_project_filtered.cleaned_data['project_name',campus_partner='camp_partner',
        #total_hours='tot_hrs',total_people= 'tot_peop' ,wages = 'wage_peop'])
        #NameOfCampusPartner = CampusPartnerUser.objects.all().filter()
        #print(project_details)
        # print(form.errors)
        # if form.is_valid():
        #     if(Project.objects.all().filter(project_name=form.cleaned_data['project_name']).exists()):
        #         theProject= Project.objects.all().filter(project_name=form.cleaned_data['project_name'])
        #         return render(request,'projects/SearchProject.html', {'form':ProjectSearchForm(),'searchedProject':theProject})
        return render(request,'projects/SearchProject.html',{'filter': searched_project,'projectNames':names,'searchedProject':project_details, 'theList':yesNolist})


@login_required()
def SearchForProjectAdd(request,pk):
    foundProject = None
    names = []
    for project in Project.objects.all():
        names.append(project.project_name)
    print(request.user.id)
    campusUserProjectsNames = []
    campusPartnerProjects = ProjectCampusPartner.objects.all()
    for project in ProjectCampusPartner.objects.all():
        campusUserProjectsNames.append(project.project_name)

    for project in Project.objects.all():
        if project.pk == int(pk):
            foundProject = project

    cp = CampusPartnerUser.objects.filter(user_id=request.user.id)
    print("HERE ")
    print(cp)
    object = ProjectCampusPartner(project_name=foundProject, campus_partner=cp)
    object.save()
    return redirect("proj_view_user")


# List Projects for Public View


def projectsPublicReport(request):
    
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    projectsData = []
    for project in projects.qs:
        projectMissions = ProjectMission.objects.filter(project_name=project)
        data = {}
        for mission in projectMissions:
            if mission in missions.qs:
                data['projectName'] = project.project_name
                data['engagementType'] = project.engagement_type

                try:
                    projectCampusPartners = ProjectCampusPartner.objects.filter(project_name=project.id)
                    for projectCampusPartner in projectCampusPartners:
                        if "campusPartner" in data:
                            data['campusPartner'] = data['campusPartner'] + ", " + str(projectCampusPartner.campus_partner)
                        else:
                            data['campusPartner'] = projectCampusPartner.campus_partner
                except ProjectCampusPartner.DoesNotExist:
                    data['campusPartner'] = None

                if data['campusPartner']:
                    try:
                        projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name=project.id)
                        for projectCommunityPartner in projectCommunityPartners:
                            if projectCommunityPartner.community_partner in communityPartners.qs:
                                if "communityPartner" in data:
                                    data['communityPartner'] = data['communityPartner'] + ", " + str(projectCommunityPartner.community_partner)
                                else:
                                    data['communityPartner'] = projectCommunityPartner.community_partner
                    except ProjectCommunityPartner.DoesNotExist:
                        data['communityPartner'] = ""
                break

        if data:
            projectsData.append(data)

    return render(request, 'reports/projects_public_view.html', {'projects': projects,
                  'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners})


# List of community Partners Public View 

def communityPublicReport(request):
    
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityData = []

    for partner in communityPartners.qs:
        data={}
        data["name"] = partner.name
        communityProjects = ProjectCommunityPartner.objects.filter(community_partner=partner.id)
        count = 0
        for cproject in communityProjects:
            project = cproject.project_name
            projectMissions = ProjectMission.objects.filter(project_name=project)
            if project in projects.qs:
                count +=1
            for mission in projectMissions:
                if mission in missions.qs and count == 0:
                    count +=1
        data['communityProjects'] = count
        communityData.append(data)


    return render(request, 'reports/community_public_view.html',
                   {'communityPartners': communityPartners, "projects": projects, 
                    'communityData': communityData, 'missions': missions})


# List Projects for Private View 
@login_required()
def projectsPrivateReport(request):

    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    projectsData = []
    for project in projects.qs:
        projectMissions = ProjectMission.objects.filter(project_name=project)
        data = {}
        for mission in projectMissions:
            if mission in missions.qs:
                data['projectName'] = project.project_name
                data['engagementType'] = project.engagement_type
                data['total_UNO_students'] = project.total_uno_students
                data['total_hours'] = project.total_uno_hours
                data['economic_impact'] = project.total_economic_impact

                try:
                    projectCampusPartners = ProjectCampusPartner.objects.filter(project_name=project.id)
                    for projectCampusPartner in projectCampusPartners:
                        if "campusPartner" in data:
                            data['campusPartner'] = data['campusPartner'] + ", " + str(projectCampusPartner.campus_partner)
                        else:
                            data['campusPartner'] = projectCampusPartner.campus_partner
                except ProjectCampusPartner.DoesNotExist:
                    data['campusPartner'] = None

                if data['campusPartner']:
                    try:
                        projectCommunityPartners = ProjectCommunityPartner.objects.filter(project_name=project.id)
                        for projectCommunityPartner in projectCommunityPartners:
                            if projectCommunityPartner.community_partner in communityPartners.qs:
                                if "communityPartner" in data:
                                    data['communityPartner'] = data['communityPartner'] + ", " + str(projectCommunityPartner.community_partner)
                                else:
                                    data['communityPartner'] = projectCommunityPartner.community_partner
                    except ProjectCommunityPartner.DoesNotExist:
                        data['communityPartner'] = ""
                break

        if data:
            projectsData.append(data)


    return render(request, 'reports/projects_private_view.html', {'projects': projects,
                  'projectsData': projectsData, "missions": missions, "communityPartners": communityPartners})

@login_required()
def communityPrivateReport(request):

    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    missions = ProjectMissionFilter(request.GET, queryset=ProjectMission.objects.all())
    communityData = []

    for partner in communityPartners.qs:
        data={}
        data["name"] = partner.name
        data['website'] = partner.website_url
        try:
            contact = Contact.objects.get(community_partner=partner, contact_type='Primary')
        except Contact.DoesNotExist:
            contact = None
        
        if contact:
            data['email'] = contact.email_id
        else:
            data['email'] = ""

        communityProjects = ProjectCommunityPartner.objects.filter(community_partner=partner.id)
        count = 0
        for cproject in communityProjects:
            project = cproject.project_name
            projectMissions = ProjectMission.objects.filter(project_name=project)
            if project in projects.qs:
                project = Project.objects.get(id=cproject.id)
                if "total_hours" in data:
                    data['total_UNO_students'] = data['total_UNO_students'] + project.total_uno_students
                    data['total_hours'] = data['total_hours'] + project.total_uno_hours
                    data['economic_impact'] = data['economic_impact'] + project.total_economic_impact
                else:
                    data['total_UNO_students'] = project.total_uno_students
                    data['total_hours'] = project.total_uno_hours
                    data['economic_impact'] = project.total_economic_impact
                count +=1
            for mission in projectMissions:
                if mission in missions.qs and count == 0:
                    count +=1
        data['communityProjects'] = count
        communityData.append(data)

    return render(request, 'reports/community_private_view.html',
                   {'communityPartners': communityPartners, "projects": projects, 
                    'communityData': communityData, 'missions': missions})

