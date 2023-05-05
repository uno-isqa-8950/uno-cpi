import pandas as pd

from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from home.decorators import campuspartner_required
from home.forms import UserForm, CampusPartnerAvatar
from projects.forms import ProjectForm
from .forms import *
from .models import CampusPartner as CampusPartnerModel
from projects.models import *
from partners.models import *
from home.models import *
from home.forms import userUpdateForm, userCommUpdateForm
from django.template.loader import render_to_string
import googlemaps
from shapely.geometry import shape, Point
from django.conf import settings
from googlemaps import Client
from django.urls import reverse
# from projects.views import editProject

from django.core.cache import cache

# import pandas as pd
import json

gmaps = Client(key=settings.GOOGLE_MAPS_API_KEY)
import os


def countyGEO():
    with open('home/static/GEOJSON/NEcounties2.geojson') as f:
        geojson1 = json.load(f)

    county = geojson1["features"]
    return county


##### Get the district GEOJSON ##############
def districtGEO():
    with open('home/static/GEOJSON/ID3.geojson') as f:
        geojson = json.load(f)

    district = geojson["features"]
    return district


countyData = countyGEO()
district = districtGEO()


def registerCampusPartner(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    colleges = []
    data_definition = DataDefinition.objects.all()
    for object in College.objects.order_by('college_name'):
        colleges.append(object.college_name)
    # departmnts = []
    # for object in Department.objects.order_by('department_name'):
    #    departmnts.append(object.department_name)

    if request.method == 'POST':
        # cache.clear()
        campus_partner_form = CampusPartnerForm(request.POST)
        formset = ContactFormset(request.POST or None)
        if campus_partner_form.is_valid() and formset.is_valid():
            campus_partner = campus_partner_form.save()
            contacts = formset.save(commit=False)
            for contact in contacts:
                contact.campus_partner = campus_partner
                contact.save()
            return render(request, 'registration/campus_partner_register_done.html')

    else:
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
    return render(request, 'registration/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'data_definition': data_definition,
                   'formset': formset, 'colleges': colleges})


def registerCommunityPartner(request):
    # ContactFormsetCommunity = modelformset_factory(Contact, extra=1, form=CommunityContactForm)
    comm_partner_mission = modelformset_factory(CommunityPartnerMission, extra=1, form=CommunityMissionFormset)
    prim_comm_partner_mission = modelformset_factory(CommunityPartnerMission, extra=1,
                                                     form=PrimaryCommunityMissionFormset)
    data_definition = DataDefinition.objects.all()
    commType = []
    for object in CommunityType.objects.order_by('community_type'):
        commType.append(object.community_type)

    if request.method == 'POST':
        # cache.clear()
        community_partner_form = CommunityPartnerForm(request.POST)
        formset_primary_mission = prim_comm_partner_mission(request.POST or None, prefix='primary_mission')
        formset_mission = comm_partner_mission(request.POST or None, prefix='mission')
        # formset = ContactFormsetCommunity(request.POST or None, prefix='contact')

        if community_partner_form.is_valid() and formset_mission.is_valid() and formset_primary_mission.is_valid():
            community_partner = community_partner_form.save()
            # contacts = formset.save(commit=False)
            primary_missions = formset_primary_mission.save(commit=False)
            missions = formset_mission.save(commit=False)

            for primary_mission in primary_missions:
                primary_mission.community_partner = community_partner
                missionarea = primary_mission.mission_area
                primary_mission.mission_type = 'Primary'
                primary_mission.save()
            for mission in missions:
                mission.community_partner = community_partner
                missionarea = mission.mission_area
                mission.mission_type = 'Other'
                mission.save()
            # for contact in contacts:
            #     contact.community_partner = community_partner
            #     contact.save()

            return render(request, 'registration/community_partner_register_done.html', )

    else:
        community_partner_form = CommunityPartnerForm()
        # formset = ContactFormsetCommunity(queryset=Contact.objects.none(), prefix='contact')
        formset_mission = comm_partner_mission(queryset=CommunityPartnerMission.objects.none(), prefix='mission')
        formset_primary_mission = prim_comm_partner_mission(queryset=CommunityPartnerMission.objects.none(),
                                                            prefix='primary_mission')

    return render(request,
                  'registration/community_partner_register.html',
                  {'community_partner_form': community_partner_form,
                   'data_definition': data_definition,
                   'formset_mission': formset_mission, 'commType': commType,
                   'formset_primary_mission': formset_primary_mission}, )


# validation for community name in register community partner form
def ajax_load_community(request):
    name = request.GET.get('name', None)

    data = {
        'is_taken': CommunityPartner.objects.filter(name__iexact=name).exists()
    }
    return JsonResponse(data)


# validation for acronym
# def ajax_load_community_acronym(request):
#     acronym = request.GET.get('acronym', None)
#     print(acronym)
#     data = {
#         'is_taken': CommunityPartner.objects.filter(acronym__iexact=acronym).exists()
#     }
#     return JsonResponse(data)


# validation for campus name in register community partner form
def ajax_load_campus(request):
    name = request.GET.get('name', None)
    data = {
        'is_taken': CampusPartner.objects.filter(name__iexact=name).exists()
    }
    return JsonResponse(data)


# Campus and Community Partner user Profile
@login_required
def userProfile(request):
    if request.user.is_campuspartner:
        # campus_user = get_object_or_404(CampusPartnerUser, user= request.user.id)
        return render(request,
                      'partners/campus_partner_user_profile.html', )  # {"campus_partner_name": str(campus_user.campus_partner)})

    elif request.user.is_communitypartner:
        # community_user = get_object_or_404(CommunityPartnerUser, user= request.user.id)
        return render(request,
                      'partners/community_partner_user_profile.html')  # {"community_partner_name": str(community_user.community_partner)})


# Campus and Community Partner User Update Profile

@login_required
def userProfileUpdate(request):
    user = get_object_or_404(User, id=request.user.id)

    if request.user.is_campuspartner:

        if request.method == 'POST':
            request.POST._mutable = True
            request.POST['first_name'] = request.POST['First Name']
            request.POST['last_name'] = request.POST['Last Name']
            request.POST['email'] = request.POST['Email']
            request.POST._mutable = False

            user_form = userUpdateForm(data=request.POST, instance=user)
            # avatar_form = CampusPartnerAvatar(data=request.POST, files=request.FILES, instance=user)

            if user_form.is_valid():  # and avatar_form.is_valid():
                user_form.save()
                # avatar_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('partners:userprofile')

        else:
            user_form = userUpdateForm(instance=user)
            # avatar_form = CampusPartnerAvatar(instance=user)

        return render(request,
                      'partners/campus_partner_user_update.html',
                      {'user_form': user_form})  # 'avatar_form': avatar_form

    elif request.user.is_communitypartner:

        if request.method == 'POST':

            user_form = userCommUpdateForm(data=request.POST, instance=user)
            # avatar_form = CampusPartnerAvatar(data=request.POST, files=request.FILES, instance=user)

            if user_form.is_valid():  # and avatar_form.is_valid():
                user_form.save()
                # avatar_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('partners:userprofile')

        else:
            user_form = userCommUpdateForm(instance=user)
            # avatar_form = CampusPartnerAvatar(instance=user)

        return render(request,
                      'partners/community_partner_user_update.html',
                      {'user_form': user_form})  # 'avatar_form': avatar_form


# Campus and Community Partner org Profile

@login_required
def orgProfile(request):
    if request.user.is_communitypartner:
        community_user = CommunityPartnerUser.objects.filter(user=request.user.id)
        community_partners = []
        for user in community_user:
            community_partner = CommunityPartner.objects.filter(name=user.community_partner)
            community_partners.extend(community_partner)
            final = community_partners
        # for mission in missions:
        #     mission['mission_area'] = str(MissionArea.objects.only('mission_name').get(id = mission['mission_area_id']))

        return render(request, 'partners/community_partner_org_profile.html', {"final": final})
    elif request.user.is_campuspartner:
        campus_user = CampusPartnerUser.objects.filter(user=request.user.id)
        campus_partner = []
        for user in campus_user:
            campus_partner1 = CampusPartner.objects.filter(name=user.campus_partner)
            campus_partner.extend(campus_partner1)
            final = campus_partner
        return render(request, 'partners/campus_partner_org_profile.html', {"final": final})
    elif request.user.is_superuser:
        # adding both campus and community partner in list for superuser to make it work 
        # or else link will get error after switching from Campus/community drop down to Admin view
        campus_partner1 = CampusPartner.objects.all()
        community_partner = CommunityPartner.objects.all()
        all_partner = []
        all_partner.extend(campus_partner1)
        all_partner.extend(community_partner)
        final = community_partner
        return render(request, 'partners/campus_partner_org_profile.html', {"final": final})


# Campus and Community Partner org Update Profile
@login_required
def orgProfileUpdate(request, pk):
    if request.user.is_communitypartner:
        community_partner = get_object_or_404(CommunityPartner, pk=pk)

        if request.method == 'POST':
            community_org_form = CommunityPartnerUpdateForm(data=request.POST, instance=community_partner)

            if community_org_form.is_valid():
                community_org_form.save()
                messages.success(request, 'Organization profile was successfully updated!')
                return redirect('partners:orgprofile')

        else:
            community_org_form = CommunityPartnerUpdateForm(instance=community_partner)

        return render(request,
                      'partners/community_partner_org_update.html', {'community_org_form': community_org_form
                                                                     })

    elif request.user.is_campuspartner:
        campus_partner = get_object_or_404(CampusPartner, pk=pk)

        if request.method == 'POST':
            campus_org_form = CampusPartnerForm(data=request.POST, instance=campus_partner)

            if campus_org_form.is_valid():
                campus_org_form.save()
                messages.success(request, 'Organization profile was successfully updated!')
                return redirect('partners:orgprofile')

        else:
            campus_org_form = CampusPartnerForm(instance=campus_partner)
            # contacts_form = CampusPartnerContactForm(instance=contacts)

        return render(request,
                      'partners/campus_partner_org_update.html', {'campus_org_form': campus_org_form
                                                                  })


# adds a new organisation for the logged user
def PartnerAdd(request):
    if request.user.is_campuspartner:
        if request.method == "POST":
            form = CampusPartnerAddForm(request.POST)
            if form.is_valid():
                form.user = request.user
                CampusPartnerAdd = form.save(commit=False)
                CampusPartnerAdd.user = request.user
                CampusPartnerAdd.save()
                return redirect('partners:orgprofile')
        else:
            form = CampusPartnerAddForm()
        return render(request, 'partners/campus_partner_org_add.html', {'form': form})

    elif request.user.is_communitypartner:
        if request.method == "POST":
            form = CommunityPartnerAddForm(request.POST)
            if form.is_valid():
                form.user = request.user
                CommunityPartnerAdd = form.save(commit=False)
                CommunityPartnerAdd.user = request.user
                CommunityPartnerAdd.save()
                return redirect('partners:orgprofile')
        else:
            form = CommunityPartnerAddForm()
        return render(request, 'partners/community_partner_org_add.html', {'form': form})
    else:
        return redirect('/admin')


# Shows contacts of a particular Campus Partner/Community Partner in the Organizations tab of a User
def orgProfileContacts(request, pk):
    if request.user.is_campuspartner:
        campus_partner = get_object_or_404(CampusPartner, pk=pk)
        contacts1 = Contact.objects.filter(campus_partner=campus_partner)
        return render(request, 'partners/campus_partner_org_contact.html', {"contacts": contacts1})
    elif request.user.is_communitypartner:
        community_partner = get_object_or_404(CommunityPartner, pk=pk)
        contacts = Contact.objects.filter(community_partner=community_partner)
        return render(request, 'partners/community_partner_org_contact.html', {"contacts": contacts})


# Shows Missions of a particular Campus Partner/Community Partner in the Organizations tab of a User
def orgProfileMissions(request, pk):
    if request.user.is_communitypartner:
        community_partner = get_object_or_404(CommunityPartner, pk=pk)
        missions = CommunityPartnerMission.objects.filter(community_partner=community_partner)
        return render(request, 'partners/community_partner_org_mission.html', {"missions": missions})


# register function for a user to register a new campus partner during filling the project create form
def registerCampusPartner_forprojects(request):
    ContactFormset = modelformset_factory(Contact, extra=1, form=CampusPartnerContactForm)
    colleges = []
    data_definition = DataDefinition.objects.all()
    for object in College.objects.order_by('college_name'):
        colleges.append(object.college_name)
    # departmnts = []
    # for object in Department.objects.order_by('department_name'):
    #    departmnts.append(object.department_name)

    if request.method == 'POST':
        # cache.clear()
        projectId = request.POST.get('projectId')
        campus_partner_form = CampusPartnerForm(request.POST)

        formset = ContactFormset(request.POST or None)

        if campus_partner_form.is_valid() and formset.is_valid():
            campus_partner = campus_partner_form.save()
            contacts = formset.save(commit=False)
            for contact in contacts:
                contact.campus_partner = campus_partner
                contact.save()
            return redirect('editProject', pk=projectId)

    else:
        projectId = request.GET.get('projectId')
        campus_partner_form = CampusPartnerForm()
        formset = ContactFormset(queryset=Contact.objects.none())
        return render(request, 'registration/campus_partner_register_for_projects.html',
                      {'campus_partner_form': campus_partner_form, 'data_definition': data_definition,
                       'formset': formset, 'colleges': colleges, 'projectId': projectId})


# register function for a user to register a new community partner during filling the project create form
def registerCommunityPartner_forprojects(request):
    # ContactFormsetCommunity = modelformset_factory(Contact, extra=1, form=CommunityContactForm)
    comm_partner_mission = modelformset_factory(CommunityPartnerMission, extra=1, form=CommunityMissionFormset)
    prim_comm_partner_mission = modelformset_factory(CommunityPartnerMission, extra=1,
                                                     form=PrimaryCommunityMissionFormset)
    data_definition = DataDefinition.objects.all()
    commType = []
    for object in CommunityType.objects.order_by('community_type'):
        commType.append(object.community_type)

    if request.method == 'POST':
        # cache.clear()
        projectId = request.POST.get('projectId')
        community_partner_form = CommunityPartnerForm(request.POST)
        formset_primary_mission = prim_comm_partner_mission(request.POST or None, prefix='primary_mission')
        formset_mission = comm_partner_mission(request.POST or None, prefix='mission')
        # formset = ContactFormsetCommunity(request.POST or None, prefix='contact')

        if community_partner_form.is_valid() and formset_mission.is_valid() and formset_primary_mission.is_valid():
            community_partner = community_partner_form.save()
            # contacts = formset.save(commit=False)
            primary_missions = formset_primary_mission.save(commit=False)
            missions = formset_mission.save(commit=False)
            print('entered form')
            for primary_mission in primary_missions:
                primary_mission.community_partner = community_partner
                missionarea = primary_mission.mission_area
                primary_mission.mission_type = 'Primary'
                primary_mission.save()
            for mission in missions:
                mission.community_partner = community_partner
                missionarea = mission.mission_area
                mission.mission_type = 'Other'
                mission.save()
            return redirect('editProject', pk=projectId)

    else:
        projectId = request.GET.get('projectId')
        community_partner_form = CommunityPartnerForm()
        # formset = ContactFormsetCommunity(queryset=Contact.objects.none(), prefix='contact')
        formset_mission = comm_partner_mission(queryset=CommunityPartnerMission.objects.none(), prefix='mission')
        formset_primary_mission = prim_comm_partner_mission(queryset=CommunityPartnerMission.objects.none(),
                                                            prefix='primary_mission')

        return render(request,
                      'registration/community_partner_register_for_projects.html',
                      {'community_partner_form': community_partner_form,
                       'data_definition': data_definition,
                       'formset_mission': formset_mission, 'commType': commType,
                       'formset_primary_mission': formset_primary_mission, 'projectId': projectId}, )


def checkCommunityPartner(request):
    partnerForm = ProjectForm()
    communityParnterName = []

    for object in CommunityPartner.objects.order_by('name', 'acronym'):
        partner = object.name
        if (object.acronym is not None):
            partner = partner + " (" + (object.acronym) + ")"

        if partner not in communityParnterName:
            communityParnterName.append(partner)
            print(partner)

    if request.method == 'POST':
        partnerForm = ProjectForm(request.POST)

    # print(projectNames)
    return render(request, 'partners/checkCommunityPartner.html',
                  {'partnerForm': partnerForm, 'partnerNames': communityParnterName})
