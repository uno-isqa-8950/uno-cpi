from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from projects.models import *
from home.models import *
from partners.models import *
from .forms import ProjectCommunityPartnerForm
from django.contrib.auth.decorators import login_required
from itertools import chain

from .models import Project,ProjectMission ,ProjectCommunityPartner ,ProjectCampusPartner ,Status ,EngagementType,ActivityType
from .forms import ProjectForm, ProjectMissionForm
from django.shortcuts import render, get_object_or_404 , get_list_or_404
from django.utils import timezone
from  .forms import ProjectMissionFormset,ProjectCommunityPartnerForm2, ProjectCampusPartnerForm,ProjectForm2
from django.forms import inlineformset_factory, modelformset_factory



def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)
#    print(usertype.is_communitypartner)
#    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome,'usertype':usertype})


def communitypartnerproject(request):
    projects = Project.objects.all()
    p_missions = ProjectMission.objects.all()
    return render(request, 'projects/community_partner_projects.html',
                  {'projects': projects, 'p_missions': p_missions})


def communitypartnerproject_edit(request,pk):
    print('test1')
    project = get_object_or_404(Project, pk=pk)
    print('test2')
    if request.method == "POST":
        print('test3')
        form = ProjectCommunityPartnerForm(request.POST,instance=project)
        if form.is_valid():
            project = form.save()
            project.updated_date = timezone.now()
            project.save()
            projects = Project.objects.filter()
            return render(request, 'community_partner_projects.html',
                          {'projects': projects})
    else:
        form = ProjectCommunityPartnerForm(instance=project)
        return render(request, 'community_partner_projects_edit.html', {'form': form})




def project_list(request):
   project = Project.objects.filter(created_date__lte=timezone.now())
   projects_list=[]
   for x in project:
     projmisn= list(ProjectMission.objects.filter(project_name_id = x.id))
     cp= list(ProjectCommunityPartner.objects.filter(project_name_id = x.id))
     camp_part= list(ProjectCampusPartner.objects.filter(project_name_id = x.id))

     data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type, 'activityType': x.activity_type,
           'facilitator': x.facilitator, 'semester': x.semester, 'status':x.status,'startDate': x.start_date,
           'endDate': x.end_date,'total_uno_students':x.total_uno_students,'total_uno_hours':x.total_uno_hours,
             'total_k12_students': x.total_k12_students,'total_k12_hours': x.total_k12_hours, 'total_uno_faculty': x.total_uno_faculty,
             'total_other_community_members':x.total_other_community_members,'outcomes':x.outcomes,'total_economic_impact':x.total_economic_impact,
                         'projmisn': projmisn,'cp':cp , 'camp_part':camp_part}
     projects_list.append(data)

   return render(request, 'projects/Project_list.html',{'project': projects_list})

def project_total_Add(request):
    mission_details = modelformset_factory(ProjectMission, extra =1 , form = ProjectMissionFormset)
    proj_comm_part= modelformset_factory(ProjectCommunityPartner, extra=1 , form =ProjectCommunityPartnerForm2)
    proj_campus_part=modelformset_factory(ProjectCampusPartner, extra=1, form=ProjectCampusPartnerForm)

    if request.method == 'POST':
        project = ProjectForm2(request.POST)
        formset = mission_details(request.POST or None)
        formset2 = proj_comm_part(request.POST or None)
        formset3 = proj_campus_part(request.POST or None)


        if project.is_valid() and formset.is_valid() and formset2.is_valid():
            proj= project.save()
            mission_form = formset.save(commit = False)
            proj_comm_form = formset2.save(commit= False)
            proj_campus_form = formset3.save(commit=False)

            for k in proj_comm_form:
                k.project = proj
                # print("in add comm")
                print(k.project)
                k.save()
            for form in mission_form:
                form.project_name = proj
                # print("in add mission")
                print(form.project_name)
                form.save()
            for c in proj_campus_form:
                c.project = proj
                # print("in add campus")
                print(c.project)
                c.save()

                project = Project.objects.filter(created_date__lte=timezone.now())
            projects_list = []

            for x in project:
                projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                cp = list(ProjectCommunityPartner.objects.filter(project_id=x.id))
                camp_part = list(ProjectCampusPartner.objects.filter(project_id=x.id))

                data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                        'activityType': x.activity_type,
                        'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                        'startDate': x.start_date,
                        'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                        'total_uno_hours': x.total_uno_hours,
                        'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                        'total_uno_faculty': x.total_uno_faculty,
                        'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                        'total_economic_impact': x.total_economic_impact,
                        'projmisn': projmisn, 'cp': cp, 'camp_part': camp_part}
                projects_list.append(data)
            return render(request, 'projects/Project_list.html', {'project':projects_list } )

    else:
        project = ProjectForm2()
        formset = mission_details(queryset=ProjectMission.objects.none())
        formset2 = proj_comm_part(queryset=ProjectCommunityPartner.objects.none())
        formset3 = proj_campus_part(queryset=ProjectCampusPartner.objects.none())
    return render(request,
                          'projects/project_add.html',{'project': project, 'formset': formset, 'formset2':formset2, 'formset3': formset3})



def project_edit_new(request,pk):

    mission_edit_details = inlineformset_factory(Project,ProjectMission, extra=0, form=ProjectMissionFormset)
    proj_comm_part_edit = inlineformset_factory(Project,ProjectCommunityPartner, extra=0, form=ProjectCommunityPartnerForm2)
    proj_campus_part_edit = inlineformset_factory(Project,ProjectCampusPartner, extra=0, form=ProjectCampusPartnerForm)
    # print('print input to edit')
    # print(pk)
    # print(request)
    if request.method == 'POST':
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)
            #print("in for loop")
        formset_missiondetails = mission_edit_details(request.POST ,request.FILES, instance =x)
        formset_comm_details = proj_comm_part_edit(request.POST, request.FILES, instance=x)
        formset_camp_details = proj_campus_part_edit(request.POST, request.FILES, instance=x)

        if project.is_valid() and formset_missiondetails.is_valid() and formset_comm_details.is_valid() and formset_camp_details.is_valid():

            instances = project.save()
            pm = formset_missiondetails.save(commit=False)
            compar= formset_comm_details.save(commit=False)
            campar= formset_camp_details.save(commit=False)

            for k in pm:
                k.project_name = instances
                k.save()
            for p in compar:
                p.project= instances
                p.save()
            for l in campar:
                l.project= instances
                l.save()
            project = Project.objects.filter(created_date__lte=timezone.now())
            projects_list = []

            for x in project:
                projmisn = list(ProjectMission.objects.filter(project_name_id=x.id))
                cp = list(ProjectCommunityPartner.objects.filter(project_id=x.id))
                camp_part = list(ProjectCampusPartner.objects.filter(project_id=x.id))

                data = {'pk': x.pk, 'name': x.project_name, 'engagementType': x.engagement_type,
                        'activityType': x.activity_type,
                        'facilitator': x.facilitator, 'semester': x.semester, 'status': x.status,
                        'startDate': x.start_date,
                        'endDate': x.end_date, 'total_uno_students': x.total_uno_students,
                        'total_uno_hours': x.total_uno_hours,
                        'total_k12_students': x.total_k12_students, 'total_k12_hours': x.total_k12_hours,
                        'total_uno_faculty': x.total_uno_faculty,
                        'total_other_community_members': x.total_other_community_members, 'outcomes': x.outcomes,
                        'total_economic_impact': x.total_economic_impact,
                        'projmisn': projmisn, 'cp': cp, 'camp_part': camp_part}
                projects_list.append(data)
            return render(request, 'projects/Project_list.html', {'project': projects_list})

    else:
        #print(" Project_edit_new else")
        proj_edit = Project.objects.filter(id=pk)
        for x in proj_edit:
            project = ProjectForm2(request.POST or None, instance=x)
        proj_mission = ProjectMission.objects.filter(project_name_id=pk)
        proj_comm_part = ProjectCommunityPartner.objects.filter(project_id = pk)
        proj_camp_part = ProjectCampusPartner.objects.filter(project_id = pk)
        formset_missiondetails = mission_edit_details(instance=x)
        formset_comm_details = proj_comm_part_edit(instance=x)
        formset_camp_details = proj_campus_part_edit(instance=x)

        return render(request,'projects/project_edit.html',{'project': project,
                                               'formset_missiondetails':formset_missiondetails,
                                               'formset_comm_details': formset_comm_details,
                                               'formset_camp_details':formset_camp_details})

