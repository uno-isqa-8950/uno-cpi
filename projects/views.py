from numpy import shape
from home.decorators import communitypartner_required
from home.views import *
from partners.views import *
from home.models import *
from home.filters import *
from partners.models import *
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory, modelformset_factory
from shapely.geometry import shape, Point
import datetime
from django.conf import settings
from googlemaps import Client
# The imports below are for running sql queries for AllProjects Page
from django.db import connection
from UnoCPI import sqlfiles
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utilities import *

sql = sqlfiles

# DO NOT PUT KEY HERE, IT PULLS FROM LOCAL SETTINGS FILE
gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)


@login_required()
@communitypartner_required()
def communitypartnerhome(request):
    usertype = User.objects.get(is_communitypartner=True)
    #    if usertype.is_communitypartner == True:
    return render(request, 'community_partner_home.html',
                  {'communitypartnerhome': communitypartnerhome, 'usertype': usertype})


@login_required()
def myProjects(request):
    data_definition = DataDefinition.objects.all()
    return render(request, 'projects/myProjects.html',
                  {'project': Project.objects.filter(created_by=request.user), 'data_definition': data_definition})


def ajax_load_project(request):
    name = request.GET.get('name')
    project_year = request.GET.get('year')
    projectnameandyear = name + ': ' + project_year
    data = {
        'is_taken': Project.objects.filter(project_name__icontains=projectnameandyear).exists()
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

    project.description = description
    project.semester = start_semester
    project.end_semester = end_semester
    project.total_uno_students = uno_students
    project.total_uno_hours = uno_students_hrs
    project.k12_flag = k12_flag_value
    project.total_k12_students = k12_students
    project.total_k12_hours = k12_students_hrs
    project.project_type = project_type

    if start_academic_yr != '' and start_academic_yr is not None:
        project.academic_year = AcademicYear.objects.get(id=start_academic_yr)
        year_in_project_name = project.academic_year

    if end_academic_yr != '' and end_academic_yr is not None:
        project.end_academic_year = AcademicYear.objects.get(id=end_academic_yr)

    if engagement_type != '' and engagement_type is not None:
        project.engagement_type = EngagementType.objects.get(id=engagement_type)

    if activity_type != '' and activity_type != '0' and activity_type is not None:
        project.activity_type = ActivityType.objects.get(id=activity_type)

    if lead_staff_list != '' and lead_staff_list is not None:
        lead_name_list = []
        if lead_staff_list.find(",") != -1:
            leadName_list = lead_staff_list.split(",")
            for leadName in leadName_list:
                lead_name_list.append(leadName)
        else:
            lead_name_list.append(lead_staff_list)

        project.campus_lead_staff = lead_name_list

    project.status = Status.objects.get(name='Drafts')

    project.save()
    projectId = project.pk

    project.project_name = name + ": " + str(year_in_project_name) + " (" + str(projectId) + ")"
    project.save()

    if comm_list != '' or comm_list is not None:
        if comm_list.find(",") != -1:
            comm_Id_list = comm_list.split(",")
        else:
            comm_Id_list = comm_list

        for commId in comm_Id_list:
            comm_obj = CommunityPartner.objects.get(id=commId)
            proj_obj = Project.objects.get(id=projectId)
            projComm = ProjectCommunityPartner(project_name=proj_obj, community_partner=comm_obj)
            projComm.save()

    if campus_list != '' or campus_list is not None:
        if campus_list.find(",") != -1:
            camp_id_list = campus_list.split(",")
        else:
            camp_id_list = campus_list

        for campId in camp_id_list:
            camp_obj = CampusPartner.objects.get(id=campId)
            proj_obj = Project.objects.get(id=projectId)
            projCamp_obj = ProjectCampusPartner(project_name=proj_obj, campus_partner=camp_obj)
            projCamp_obj.save()

    data = {'save_projectId': projectId}
    return JsonResponse(data)


def saveFocusArea(request):
    selectedfocusarea = request.GET.get('focusarea')
    projectid = request.GET.get('projectId')
    print('selectedfocusarea--', selectedfocusarea)
    try:
        test = ProjectMission.objects.get(project_name_id=projectid, mission_type='Primary')
    except ProjectMission.DoesNotExist:
        test = None

    if test is not None:
        cursor = connection.cursor()
        cursor.execute(sqlfiles.editproj_updateprimarymission(),
                       (str(selectedfocusarea), str(projectid), str(projectid),))
    else:
        cursor = connection.cursor()
        cursor.execute(sqlfiles.editproj_addprimarymission(), (str(selectedfocusarea), str(projectid),))

    data = {'projectid': projectid}
    return JsonResponse(data)


def getEngagemetActivityList(request):
    selectedEngagement = request.GET.get('selectedEngagement')
    activityList = []
    if selectedEngagement is not None:
        engagementObj = EngagementType.objects.get(name=selectedEngagement)
        eng_act_obj = EngagementActivityType.objects.all().filter(EngagementTypeName=engagementObj)
        for act in eng_act_obj:
            actObj = ActivityType.objects.get(name=act.ActivityTypeName)
            activityList.append({"name": actObj.name, "id": actObj.id})

    data = {'activityList': activityList}
    return JsonResponse(data)


@login_required()
def createProject(request):
    mission_details = modelformset_factory(ProjectMission, form=ProjectMissionFormset)
    sub_category = modelformset_factory(ProjectSubCategory, extra=1, form=AddSubCategoryForm)
    proj_comm_part = modelformset_factory(ProjectCommunityPartner, extra=1, form=AddProjectCommunityPartnerForm)
    proj_campus_part = modelformset_factory(ProjectCampusPartner, extra=1, form=AddProjectCampusPartnerForm)
    data_definition = DataDefinition.objects.all()
    # Populate project name-Parimita
    request.POST.get('id_project_name')
    # if request.method == 'POST' and 'submit' in request.POST:
    if request.method == 'POST':
        project = ProjectFormAdd(request.POST)
        course = CourseForm(request.POST)
        categoryformset = sub_category(request.POST or None, prefix='sub_category')
        formset = mission_details(request.POST or None, prefix='mission')
        # formset4 = secondary_mission_details(request.POST or None, prefix='secondary_mission')
        formset2 = proj_comm_part(request.POST or None, prefix='community')
        formset3 = proj_campus_part(request.POST or None, prefix='campus')
        if project.is_valid() and formset.is_valid() and course.is_valid() and formset2.is_valid() and formset3.is_valid() and categoryformset.is_valid():

            if request.POST.get('k12_flag'):
                project.k12_flag = True
            else:
                project.k12_flag = False
            proj = project.save()
            project_name = proj.project_name.strip()

            proj.project_name = project_name + ": " + str(proj.academic_year) + " (" + str(proj.id) + ")"

            eng = str(proj.engagement_type)
            address = proj.address_line1
            stat = str(proj.status)
            if stat == 'Drafts':
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
                # return render(request, 'projects/draftadd_done.html', {'project': projects_list})
                return HttpResponseRedirect('/draft-project-done')
            elif stat == 'Active':
                proj.save()
                print(proj)
                endproject = proj

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

                try:
                    endprojectmission = ProjectMission.objects.filter(project_name__id=endproject.id)
                    print(endprojectmission)
                    for projmis in endprojectmission:
                        Project.objects.get(id=endproject.id).mission_area.add(projmis.mission)
                except Exception as e:
                    print(e)
                try:
                    endprojectcampus = ProjectCampusPartner.objects.filter(project_name__id=endproject.id)
                    for projcamp in endprojectcampus:
                        Project.objects.get(id=endproject.id).campus_partner.add(projcamp.campus_partner)
                except Exception as e:
                    print(e)
                try:
                    endprojectcommunity = ProjectCommunityPartner.objects.filter(project_name__id=endproject.id)
                    for projcom in endprojectcommunity:
                        Project.objects.get(id=endproject.id).community_partner.add(projcom.community_partner)
                except Exception as e:
                    print(e)
                try:
                    endprojectsub = ProjectSubCategory.objects.get(project_name__id=endproject.id)
                    Project.objects.get(id=endproject.id).subcategory.add(endprojectsub.sub_category)
                except Exception as e:
                    print(e)

            if request.user.is_superuser == True:
                return HttpResponseRedirect('/adminsubmit_project_done')
            else:
                return HttpResponseRedirect('/submit-project-done')

    else:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if month > 7:
            a_year = str(year) + "-" + str(year + 1)[-2:]
        else:
            a_year = str(year - 1) + "-" + str(year)[-2:]

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
                instances = project.save()
                instances.project_name = instances.project_name.split(":")[0] + ": " + str(
                    instances.academic_year) + " (" + pk + ")"
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

                    # return HttpResponseRedirect("/myDrafts")
                    return HttpResponseRedirect('/draft-project-done')
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

                if request.user.is_superuser == True:
                    # return HttpResponseRedirect('/allProjects')
                    return HttpResponseRedirect('/adminsubmit_project_done')
                else:
                    # return HttpResponseRedirect('/myProjects')
                    return HttpResponseRedirect('/submit-project-done')


    else:

        proj_edit = Project.objects.get(id=pk)

        engagementObj = proj_edit.engagement_type

        selectedActivity = proj_edit.activity_type

        eng_act_obj = EngagementActivityType.objects.all().filter(EngagementTypeName=engagementObj)

        activityList = []
        for act in eng_act_obj:

            actObj = ActivityType.objects.get(name=act.ActivityTypeName)
            # activityList.append({"name": actObj.name, "id": actObj.id})
            if str(actObj.name) == str(selectedActivity):
                selected = 'selected'
                activityList.append({"name": actObj.name, "id": actObj.id, "selected": selected})
            else:
                activityList.append({"name": actObj.name, "id": actObj.id})

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
            test = ProjectMission.objects.get(project_name_id=pk, mission_type='Primary')
        except ProjectMission.DoesNotExist:
            test = None

        if test is not None:
            proj_mission = ProjectMission.objects.get(project_name_id=pk, mission_type='Primary')
        else:
            proj_mission = 'none'

        # print(proj_mission)
        mission_areas = []
        for miss in project_all_missions:
            # print(miss.mission_name)
            if miss.mission_name == str(proj_mission):
                selected = 'selected'
                mission_areas.append({"name": miss.mission_name, "id": miss.id, 'selected': selected})
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
                                                             'project_mission': project_mission,
                                                             'mission_areas': mission_areas,
                                                             # 'formset_missiondetails': formset_missiondetails,
                                                             'formset_comm_details': formset_comm_details,
                                                             'formset_camp_details': formset_camp_details,
                                                             'formset_subcat_details': formset_subcat_details,
                                                             'projectId': pk, 'activityList': activityList,
                                                             'selectedActivity': selectedActivity,
                                                             'selectedMission': proj_mission,
                                                             'data_definition': data_definition})


@login_required()
def showAllProjects(request):
    context = filter_projects(request)
    project_list = context['project']
    paginator = Paginator(project_list, 100)  # Show 25 projects per page

    page = request.GET.get('page', 1)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    projects = paginator.get_page(page)
    return render(request, 'projects/allProjects.html',
                  {'project': projects,
                   'data_definition': context['data_definition'],
                   'missions': context['missions'],
                   'communityPartners': context['communityPartners'],
                   'campus_filter': context['campus_filter'],
                   'college_filter': context['college_filter'],
                   'campus_id': context['campus_id'],
                   'k12_choices': context['k12_choices'],
                   'k12_selection': context['k12_selection'],
                   'cec_part_choices': context['cec_part_choices'],
                   'cec_part_selection': context['cec_part_selection'],
                   'projects': context['projects'],
                   'cards': cards,
                   'parameters': parameters,
                   })


# all projects ends here

# Public reports start here
# New view for project public table and card view
def projectstablePublicReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    context = filter_projects(request)
    if selectedprojectId != None:
        filtered_ids = selectedprojectId.split(",")
        project_return = Project.objects.filter(id__in=filtered_ids)
    else:
        project_return = context['project']
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    return render(request, 'reports/projectspublictableview.html',
                  {'parameters': parameters,
                   'project': project_return,
                   'data_definition': context['data_definition'],
                   'missions': context['missions'],
                   'communityPartners': context['communityPartners'],
                   'campus_filter': context['campus_filter'],
                   'college_filter': context['college_filter'],
                   'campus_id': context['campus_id'],
                   'k12_choices': context['k12_choices'],
                   'k12_selection': context['k12_selection'],
                   'cec_part_choices': context['cec_part_choices'],
                   'cec_part_selection': context['cec_part_selection'],
                   'projects': context['projects'],
                   })


@login_required()
def SearchForProjectAdd(request, pk):
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


def projectsPublicReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    context = filter_projects(request)
    if selectedprojectId != None:
        filtered_ids = selectedprojectId.split(",")
        project_return = Project.objects.filter(id__in=filtered_ids)
    else:
        project_return = context['project']
    proj_per_page_cnt = 5
    proj_per_page = DataDefinition.objects.get(title='project_count_per_page')
    if proj_per_page is not None:
        proj_per_page_cnt = proj_per_page.description

    page = request.GET.get('page', 1)
    paginator = Paginator(project_return, proj_per_page_cnt)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    return render(request, 'reports/projects_public_view.html',
                  {'data_definition': context['data_definition'],
                   'missions': context['missions'],
                   'communityPartners': context['communityPartners'],
                   'campus_filter': context['campus_filter'],
                   'college_filter': context['college_filter'],
                   'campus_id': context['campus_id'],
                   'k12_choices': context['k12_choices'],
                   'k12_selection': context['k12_selection'],
                   'cec_part_choices': context['cec_part_choices'],
                   'cec_part_selection': context['cec_part_selection'],
                   'projects': context['projects'],
                   'cards': cards,
                   'parameters': parameters})


# project private card and table view starts here

@login_required()
def projectsPrivateReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    context = filter_projects(request)
    if selectedprojectId != None:
        filtered_ids = selectedprojectId.split(",")
        project_return = Project.objects.filter(id__in=filtered_ids)
    else:
        project_return = context['project']
    proj_per_page_cnt = 5
    proj_per_page = DataDefinition.objects.get(title='project_count_per_page')
    if proj_per_page is not None:
        proj_per_page_cnt = proj_per_page.description

    page = request.GET.get('page', 1)
    paginator = Paginator(project_return, proj_per_page_cnt)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(1)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    return render(request, 'reports/projects_public_view.html',
                  {'data_definition': context['data_definition'],
                   'missions': context['missions'],
                   'communityPartners': context['communityPartners'],
                   'campus_filter': context['campus_filter'],
                   'college_filter': context['college_filter'],
                   'campus_id': context['campus_id'],
                   'k12_choices': context['k12_choices'],
                   'k12_selection': context['k12_selection'],
                   'cec_part_choices': context['cec_part_choices'],
                   'cec_part_selection': context['cec_part_selection'],
                   'projects': context['projects'],
                   'cards': cards,
                   'parameters': parameters})


@login_required()
def projectstablePrivateReport(request):
    selectedprojectId = request.GET.get('proj_id_list', None)
    context = filter_projects(request)
    if selectedprojectId != None:
        filtered_ids = selectedprojectId.split(",")
        project_return = Project.objects.filter(id__in=filtered_ids)
    else:
        project_return = context['project']
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    return render(request, 'reports/projectsprivatetableview.html',
                  {'parameters': parameters,
                   'project': project_return,
                   'data_definition': context['data_definition'],
                   'missions': context['missions'],
                   'communityPartners': context['communityPartners'],
                   'campus_filter': context['campus_filter'],
                   'college_filter': context['college_filter'],
                   'campus_id': context['campus_id'],
                   'k12_choices': context['k12_choices'],
                   'k12_selection': context['k12_selection'],
                   'cec_part_choices': context['cec_part_choices'],
                   'cec_part_selection': context['cec_part_selection'],
                   'projects': context['projects'],
                   })


# Project private reports card and table view end here.


def communityPublicReport(request):
    community_dict = {}
    community_list = []
    data_list = []
    legislative_choices = []
    legislative_search = ''
    data_definition = DataDefinition.objects.all()
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    status_draft = Status.objects.filter(name='Drafts')

    comm_ids = request.GET.get('comm_ids', None)
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        if legislative_selection == '-1':
            legislative_search = '%'
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

    # cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    cec_part_selection = request.GET.get('weitz_cec_part', None)
    # cec_part_init_selection = "All"
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        # cec_part_selection = cec_part_init_selection
        cec_part_cond = '%'
    elif cec_part_selection == "CURR_COMM":
        cec_part_cond = 'Current'

    elif cec_part_selection == "FORMER_COMM":
        cec_part_cond = 'Former'

    if comm_ids is not None:
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

        data_list.append({"community_name": obj[0], "community_mission": obj[1], "project_count": obj[2],
                          "project_id_list": proj_idList, "website": obj[3], "CommStatus": obj[4]})

    cursor.close()
    return render(request, 'reports/community_public_view.html',
                  {'college_filter': college_partner_filter, 'campus_filter': campus_project_filter,
                   'project_filter': project_filter,
                   'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,
                   'communityPartners': communityPartners,
                   'community_list': community_list,
                   'communityData': data_list,
                   'data_definition': data_definition,
                   'campus_id': campus_id,
                   'cec_part_choices': cec_part_choices})


@login_required()
def communityPrivateReport(request):
    community_dict = {}
    data_list = []
    community_list = []
    legislative_choices = []
    legislative_search = ''
    # comp_part_contact = []
    data_definition = DataDefinition.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all())
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())

    # set legislative_selection on template choices field -- Manu Start
    legislative_selection = request.GET.get('legislative_value', None)

    if legislative_selection is None:
        legislative_selection = 'All'

    # legislative_choices.append('All')
    for i in range(1, 50):
        legistalive_val = 'Legislative District ' + str(i)
        legislative_choices.append(legistalive_val)

    if legislative_selection is not None and legislative_selection != 'All':
        if legislative_selection == '-1':
            legislative_search = '%'
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
        campus_id = 0
    else:
        campus_partner_cond = campus_partner_filter
        campus_id = int(campus_partner_filter)

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection is None or cec_part_selection == "All" or cec_part_selection == '':
        cec_part_cond = '%'
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
        proj_ids = obj[4]
        proj_idList = ''
        sum_uno_students = 0
        sum_uno_hours = 0
        if proj_ids is not None:
            name_count = 0
            if len(proj_ids) > 0:
                for i in proj_ids:
                    cursor.execute(
                        "Select p.total_uno_students , p.total_uno_hours from projects_project p where p.id=%s",
                        (str(i),))
                    for obj1 in cursor.fetchall():
                        sum_uno_students = sum_uno_students + obj1[0]
                        sum_uno_hours = sum_uno_hours + obj1[1]
                    proj_idList = proj_idList + str(i)
                    if name_count < len(proj_ids) - 1:
                        proj_idList = proj_idList + str(",")
                        name_count = name_count + 1

        data_list.append(
            {"CommunityName": obj[0], "mission": obj[1], "Projects": obj[2], "numberofunostudents": sum_uno_students,
             "unostudentshours": sum_uno_hours, "website": obj[3], "proj_id_list": proj_idList, "CommStatus": obj[5]})

    cursor.close()
    return render(request, 'reports/community_private_view.html',
                  {'college_filter': college_partner_filter, 'project_filter': project_filter,
                   'data_definition': data_definition,
                   'legislative_choices': legislative_choices, 'legislative_value': legislative_selection,
                   'communityPartners': communityPartners,
                   'community_list': community_list,
                   'communityData': data_list,
                   'campus_filter': campus_project_filter, 'campus_id': campus_id,
                   'cec_part_choices': cec_part_choices})


# project duplication check
def checkProject(request):
    data_list = []
    flag = 0
    data_definition = DataDefinition.objects.all()
    academic_yr_filter = AcademicYear.objects.all().order_by('-academic_year')
    campus_filter = CampusPartner.objects.all()
    Community_filter = CommunityPartner.objects.all()

    if request.method == 'POST':
        flag = 0
        projectName = request.POST['projectName'].strip()
        communityPartner = request.POST['communityPartner']
        if communityPartner == 'All':
            communityPartner_id = -1
        else:
            communityPartner_id = 0
        campusPartner = request.POST['campusPartner']
        if campusPartner == 'All':
            campusPartner_id = -1
        else:
            campusPartner_id = 0
        academicYear = request.POST['academicYear']
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

        if academicYear is None or academicYear == '':
            academic_start_year_cond = int(max_yr_id)
            academic_end_year_cond = 1
            # academic_start_year_cond = int(default_yr_id)
            # academic_end_year_cond = int(default_yr_id)
            acad_id = 0

        elif academicYear == "All":
            academic_start_year_cond = int(max_yr_id)
            academic_end_year_cond = 1
            acad_id = -1
        else:
            academic_year_filter = AcademicYear.objects.get(academic_year=academicYear).id
            academic_start_year_cond = int(academic_year_filter)
            academic_end_year_cond = int(academic_year_filter)
            acad_id = 0

        commpart_filter = communityPartner.replace('All', '')
        camp_filter = campusPartner.replace('All', '')
        acad_filter = academicYear.replace('All', '')
        #  academic_filter_qs = AcademicYear.objects.get(academic_year=academicYear)
        #  acad = academic_filter_qs.id
        #  acad_id = str(acad)
        # # acad_id = [m.id for m in academic_filter_qs]
        #  print(acad_id)

        cursor = connection.cursor()

        # The % are wildcard characters. So if a project is named %test% then it would find any project with test in it. ie. thistest hitesthi
        cursor.execute(sqlfiles.checkProjectsql(), (
            "%" + projectName + "%", "%" + commpart_filter + "%", "%" + camp_filter + "%", academic_start_year_cond,
            academic_end_year_cond,))

        rows = cursor.fetchall()

        # print(rows[0][0])
        if (rows != []):

            for obj in rows:
                proj_names = obj[0]
                name = ''
                try:
                    Projectname = proj_names.split(':')
                except ValueError:
                    name = Projectname
                else:
                    for i in range(0, len(Projectname) - 1):
                        name += Projectname[i]

                proj_ids = obj[4]
                proj_idList = ''

                if proj_ids is not None:
                    name_count = 0
                    if len(proj_ids) > 0:
                        for i in proj_ids:
                            proj_idList = proj_idList + str(i)
                            if name_count < len(proj_ids) - 1:
                                proj_idList = proj_idList + str(",")
                                name_count = name_count + 1

                comm_part = obj[1]
                comm_partList = ''

                if comm_part is not None:
                    name_count = 0
                    if len(comm_part) > 0:
                        for i in comm_part:
                            comm_partList = comm_partList + str(i)
                            if name_count < len(comm_part) - 1:
                                comm_partList = comm_partList + str(",")
                                name_count = name_count + 1

                camp_part = obj[3]
                camp_partList = ''

                if camp_part is not None:
                    name_count = 0
                    if len(camp_part) > 0:
                        for i in camp_part:
                            camp_partList = camp_partList + str(i)
                            if name_count < len(camp_part) - 1:
                                camp_partList = camp_partList + str(",")
                                name_count = name_count + 1

                if (projectName.strip().lower() in obj[0].split("(")[0].strip().lower()):
                    flag = 2

                if (projectName.strip().lower() == obj[0].split("(")[0].strip().lower()):
                    flag = 1

                data_list.append(
                    {"projectName": name, "communityPartner": comm_partList, "campusPartner": camp_partList,
                     "academicYear": obj[2], "project_ids": proj_idList, 'flagBit': flag})

            return render(request, 'projects/checkProject.html',
                          {'data_list': data_list, "projectName": projectName, 'flagBit': flag,
                           'data_definition': data_definition,
                           'academic_yr_filter': academic_yr_filter,
                           'campus_filter': campus_filter,
                           'communityPartner_id': communityPartner_id,
                           "Community_filter": Community_filter,
                           'communityPartner_selected': communityPartner,
                           'campusPartner_selected': campusPartner,
                           'campusPartner_id': campusPartner_id,
                           'academicYear_selected': academicYear,
                           'acad_id': acad_id
                           })

        else:

            data_list.append({"projectName": "", "communityPartner": "", "campusPartner": "",
                              "academicYear": "", "project_ids": "", 'flagBit': flag})
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
    data_definition = DataDefinition.objects.all()
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
            mission_form = formset.save(commit=False)
            secondary_mission_form = formset4.save(commit=False)
            proj_comm_form = formset2.save(commit=False)
            sub_cat_form = categoryformset.save(commit=False)
            proj_campus_form = formset3.save(commit=False)
            for k in proj_comm_form:
                k.project_name = proj

                k.save()

            for cat in sub_cat_form:
                cat.project_name = proj

                cat.save()

            for form in mission_form:
                form.project_name = proj
                # print("in add mission")
                form.mission_type = 'Primary'
                form.save()

            for form4 in secondary_mission_form:
                form4.project_name = proj
                # print("in add secondary mission")
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
                            'total_economic_impact': x.total_economic_impact, 'projmisn': projmisn, 'cp': cp,
                            'sub': sub,
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
                  {'project': project, 'formset': formset, 'formset3': formset3, 'course': course,
                   'data_definition': data_definition,
                   'formset2': formset2, 'formset4': formset4})


###my drafts
@login_required()
def myDrafts(request):
    data_definition = DataDefinition.objects.all()
    return render(request, 'projects/myDrafts.html',
                  {'project': Project.objects.filter(created_by=request.user, status=Status.objects.get(name='Drafts')),
                   'data_definition': data_definition})


@login_required()
def drafts_delete(request, pk):
    draft_delete = get_object_or_404(Project, pk=pk)
    draft_delete.delete()
    return HttpResponseRedirect("/myDrafts")


@login_required()
def projects_delete(request, pk):
    projects_delete = get_object_or_404(Project, pk=pk)
    projects_delete.delete()
    return HttpResponseRedirect("/myProjects")


def draft_project_done(request):
    return render(request, 'projects/draftadd_done.html')


def submit_project_done(request):
    return render(request, 'projects/confirmAddProject.html')


def adminsubmit_project_done(request):
    return render(request, 'projects/adminconfirm.html')


def filter_projects(request):
    ids = []
    # if get_tenant(request).__len__() > 1:
    project_list = Project.objects.all().exclude(status__name='Drafts').order_by('-id')
    # else:
    # university = get_tenant(request)[0]
    # project_list = Project.objects.all().exclude(status__name='Drafts', university=university)
    data_definition = DataDefinition.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=Project.objects.all().exclude(status__name='Drafts'))
    communityPartners = communityPartnerFilter(request.GET, queryset=CommunityPartner.objects.all())
    campusPartners = CampusFilter(request.GET, queryset=CampusPartner.objects.all())
    campus_id = 0

    engagement_type_filter = request.GET.get('engagement_type', None)
    if engagement_type_filter is not None and engagement_type_filter != "All" and engagement_type_filter != '':
        project_list = project_list.filter(engagement_type=engagement_type_filter)

    mission_type_filter = request.GET.get('mission', None)
    if mission_type_filter is not None and mission_type_filter != "All" and mission_type_filter != '':
        project_list = project_list.filter(mission_area=mission_type_filter)

    community_type_filter = request.GET.get('community_type', None)
    if community_type_filter is not None and community_type_filter != "All" and community_type_filter != '':
        project_list = project_list.filter(community_partner__community_type=community_type_filter)

    campus_partner_filter = request.GET.get('campus_partner', None)
    if campus_partner_filter is not None and campus_partner_filter != "All" and campus_partner_filter != '':
        campus_id = int(campus_partner_filter)
        project_list = project_list.filter(campus_partner=campus_partner_filter)

    college_unit_filter = request.GET.get('college_name', None)
    if college_unit_filter is not None and college_unit_filter != "All" and college_unit_filter != '':
        project_list = project_list.filter(campus_partner__college_name=college_unit_filter)

    campus_filter = CampusPartner.objects.all()

    academic_year_filter = request.GET.get('academic_year', None)
    if academic_year_filter == None:
        academic_year_filter = AcademicYear.objects.latest('id')
    # this reads as: if the academic year filter has something in it, take all projects with that year as the
    # starting year, ending year, or a year in between, and everything after the '|' is to catch projects without an end year
    if academic_year_filter is not None and academic_year_filter != "All" and academic_year_filter != '':
        project_list = project_list.filter(academic_year_id__gte=academic_year_filter,
                                           end_academic_year__lte=academic_year_filter) \
                       | project_list.filter(academic_year=academic_year_filter)

    k12_selection = request.GET.get('k12_flag', None),
    k12_choices = K12ChoiceForm(initial={'k12_choice': k12_selection})
    K12_filter = request.GET.get('k12_flag', None)
    if K12_filter == 'Yes':
        project_list = project_list.filter(k12_flag=True)
    elif K12_filter == 'No':
        project_list = project_list.filter(k12_flag=False)

    cec_part_selection = request.GET.get('weitz_cec_part', None)
    if cec_part_selection == "CURR_COMM":
        project_list = project_list.filter(community_partner__cec_partner_status__name='Current')

    elif cec_part_selection == "FORMER_COMM":
        project_list = project_list.filter(community_partner__cec_partner_status__name='Former')

    elif cec_part_selection == "FORMER_CAMP":
        project_list = project_list.filter(campus_partner__cec_partner_status__name='Former')

    elif cec_part_selection == "CURR_CAMP":
        project_list = project_list.filter(campus_partner__cec_partner_status__name='Current')

    context = {'project': project_list,
               'data_definition': data_definition,
               'missions': ProjectMissionFilter(request.GET, queryset=MissionArea.objects.all()),
               'communityPartners': communityPartners,
               'campus_filter': campus_filter,
               'college_filter': campusPartners,
               'campus_id': campus_id,
               'k12_choices': k12_choices,
               'k12_selection': k12_selection,
               'cec_part_choices': CecPartChoiceForm(initial={'cec_choice': cec_part_selection}),
               'cec_part_selection': cec_part_selection,
               'projects': project_filter}

    return context
