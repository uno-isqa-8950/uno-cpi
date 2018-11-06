from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from projects.models import *
from home.models import *
from home.filters import *
from partners.models import *
from .forms import ProjectCommunityPartnerForm, ProjectSearchForm, ProjectCampusPartnerForm, CourseForm
from django.contrib.auth.decorators import login_required
from itertools import chain

from .models import Project,ProjectMission ,ProjectCommunityPartner ,ProjectCampusPartner ,Status ,EngagementType,ActivityType
from .forms import ProjectForm, ProjectMissionForm
from django.shortcuts import render, get_object_or_404 , get_list_or_404
from django.utils import timezone
from  .forms import ProjectMissionFormset,ProjectCommunityPartnerForm2, ProjectCampusPartnerForm,ProjectForm2
from django.forms import inlineformset_factory, modelformset_factory
from .filters import SearchProjectFilter



def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)
#    print(usertype.is_communitypartner)
#    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome,'usertype':usertype})


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
    print(proj_comm)
    for f in proj_comm:
        print(f)
        k=list(Project.objects.filter(id = f.project_name_id))
        print(k)
        for x in k:
         projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
         cp = list(ProjectCommunityPartner.objects.filter(project_name_id=x.id))
         camp = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
         proj_cam_par = list(ProjectCampusPartner.objects.filter(project_name_id=x.id))
         for proj_cam_par in proj_cam_par:
            camp_part = CampusPartner.objects.get(id=proj_cam_par.campus_partner_id)

            camp_part_names.append(camp_part)
         list_comm_part_names = comm_part_names
         comm_part_names = []
         #total_project_hours += proj_cam_par.total_hours
         #print(total_project_hours)
         data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
            'activityType': x.activity_type,
            'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
            'startDate': x.start_date,
            'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
            'total_uno_hours': x.total_uno_hours,
            'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
            'total_uno_faculty': x.total_uno_faculty,
            'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
            'total_economic_impact': x.total_economic_impact,'projmisn': projmisn, 'cp': cp, 'camp':camp, 'camp_part':list_comm_part_names
             }

         projects_list.append(data)



    return render(request, 'projects/community_partner_projects.html', {'project': projects_list})
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


def proj_view_user(request):
    #print(request.user.id)
    projects_list=[]
    camp_part_names=[]
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



def project_total_Add(request):
    mission_details = modelformset_factory(ProjectMission, extra =1 , form = ProjectMissionFormset)
    proj_comm_part= modelformset_factory(ProjectCommunityPartner, extra=1 , form =ProjectCommunityPartnerForm2)
    proj_campus_part=modelformset_factory(ProjectCampusPartner, extra=1, form=ProjectCampusPartnerForm)

    if request.method == 'POST':
        project = ProjectForm2(request.POST)
        course = CourseForm(request.POST)
        formset = mission_details(request.POST or None)
        formset2 = proj_comm_part(request.POST or None)
        formset3 = proj_campus_part(request.POST or None)


        if project.is_valid() and formset.is_valid() and formset2.is_valid():
            proj= project.save()
            course = course.save(commit=False)
            course.project_name = proj
            course.save()
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
                        'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,'description':x.description,
                        'startDate': x.start_date,
                        'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                        'total_uno_hours': x.total_uno_hours,
                        'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                        'total_uno_faculty': x.total_uno_faculty,
                        'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                        'total_economic_impact': x.total_economic_impact,
                        'projmisn': projmisn, 'cp': cp, 'camp_part': camp_part}
                projects_list.append(data)
            return render(request, 'projects/Projectlist.html', {'project':projects_list } )

    else:
        project = ProjectForm2()
        course =CourseForm()
        formset = mission_details(queryset=ProjectMission.objects.none())
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
    return render(request,
                          'projects/projectadd.html',{'project': project, 'formset': formset, 'formset2':formset2, 'formset3': formset3, 'course': course})


def project_edit_new(request,pk):

    mission_edit_details = inlineformset_factory(Project,ProjectMission, extra=0,can_delete=False, form=ProjectMissionFormset)
    proj_comm_part_edit = inlineformset_factory(Project,ProjectCommunityPartner, extra=0, can_delete=False, form=ProjectCommunityPartnerForm2)
    proj_campus_part_edit = inlineformset_factory(Project,ProjectCampusPartner, extra=0, can_delete=False,  form=ProjectCampusPartnerForm)
    #print('print input to edit')
    if request.method == 'POST':
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)
            #print("in for loop")
        formset_missiondetails = mission_edit_details(request.POST ,request.FILES, instance =x)
        formset_comm_details = proj_comm_part_edit(request.POST, request.FILES, instance=x)
        formset_camp_details = proj_campus_part_edit(request.POST, request.FILES, instance=x)
        #print("before form validations", formset_camp_details.is_valid(), formset_comm_details.is_valid())
        # print("formset_missiondetails.is_valid()8888888888", formset_missiondetails.is_valid())
        if project.is_valid() and formset_camp_details.is_valid():
            #print(" validating the forms here")
            instances = project.save()
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
                            'camp_part': list_camp_part_names
                            }

                    projects_list.append(data)
                    #print("after projects_list")

            return render(request, 'projects/Projectlist.html', {'project': projects_list})

    else:
        #print(" Project_edit_new else")
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)
        proj_mission = ProjectMission.objects.filter(project_name_id=pk)
        proj_comm_part = ProjectCommunityPartner.objects.filter(project_name_id = pk)
        proj_camp_part = ProjectCampusPartner.objects.filter(project_name_id = pk)
        formset_missiondetails = mission_edit_details(instance=x)
        formset_comm_details = proj_comm_part_edit(instance=x)
        formset_camp_details = proj_campus_part_edit(instance=x)
        print("in else project_edit 7777777")
        return render(request,'projects/projectedit.html',{'project': project,
                                               'formset_missiondetails':formset_missiondetails,
                                               'formset_comm_details': formset_comm_details,
                                               'formset_camp_details':formset_camp_details})

def SearchForProject(request):
    names=[]
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
        camp_partner = camp_part_user[0].campus_partner
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
    projectsData = []

    for mission in missions.qs:
        # import pdb; pdb.set_trace()
        print (mission.project_name)
        for project in projects.qs:
            print (project.project_name)
            if str(mission.project_name) == str(project.project_name):
                data = {}
                data['projectName'] = project.project_name
                data['engagementType'] = project.engagement_type
                try:
                    projectCommunity = ProjectCommunityPartner.objects.get(project_name=project.id)
                    data['communityPartner'] = projectCommunity.community_partner
            
                except ProjectCommunityPartner.DoesNotExist:
                    data['communityPartner'] = ""
                    # print (data['communityPartner'], "communityPartner")
        
                try:
                    projectCampus = ProjectCampusPartner.objects.get(project_name=project.id)
                    data['campusPartner'] = projectCampus.campus_partner
                    # print (data['campusPartner'], "campusPartner")
                except ProjectCampusPartner.DoesNotExist:
                    data['campusPartner'] = ""
                    # print (data['campusPartner'], "campusPartner")
                projectsData.append(data)

    return render(request, 'reports/projects_public_view.html',
                   {'filter': projects, 'projectsData': projectsData, "missions": missions})


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

