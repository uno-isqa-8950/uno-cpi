from django.shortcuts import render, redirect
from django.http import HttpResponse
from partners.models import CampusPartnerUser
from .forms import CampusPartnerForm, UniversityForm, CampusPartnerContactForm, UserForm, ProjectForm
from django.urls import reverse
import csv
from collections import OrderedDict
from .forms import *


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})

  
def cpipage(request):
    return render(request, 'home/CpiHome.html',
                  {'cpipage': cpipage})

  
def registerCampusPartnerUser(request):
    campus_partner_form = CampusPartnerForm()
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        campus_partner_form = CampusPartnerForm(request.POST)
        if user_form.is_valid() and campus_partner_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            CampusPartnerUser(campuspartner=CampusPartner.objects.filter(campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'])[0],user=new_user)
            return render(request,'home/register_done.html',)
    return render(request,
                  'home/campus_partner_user_register.html',
                  {'campus_partner_form': campus_partner_form, 'user_form': user_form})


def registerCampusPartner(request):
    if request.method == 'POST':
        campus_partner_form = CampusPartnerForm(request.POST)
        university_form = UniversityForm(request.POST)
        contact_form = CampusPartnerContactForm(request.POST)
        if campus_partner_form.is_valid() and university_form.is_valid() and contact_form.is_valid():
            # Create a new user object but avoid saving it yet
            University =  university_form.save()
            cp = CampusPartner(campus_partner_name=campus_partner_form.cleaned_data['campus_partner_name'], department_id=University)
            cp.save()
            cpc =  CampusPartnerContact(first_name=contact_form.cleaned_data['first_name'],last_name=contact_form.cleaned_data['last_name'], email_id = contact_form.cleaned_data['email_id'], partner_name =cp)
            cpc.save()
            return render(request,'home/register_done.html',)
    else:
        campus_partner_form = CampusPartnerForm()
        university_form = UniversityForm()
        contact_form = CampusPartnerContactForm()
    return render(request,
                  'home/campus_partner_register.html',
                  {'campus_partner_form': campus_partner_form, 'university_form': university_form, 'contact_form': contact_form})


def uploadCSV(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/upload_project.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    for row in reader:
        data_dict = dict(OrderedDict(row))
        # print(data_dict["mission"])
        form = ProjectForm(data_dict)
        print(form)
        if form.is_valid():
            form.save()
    return render(request, 'import/upload_project.html',
                  {'uploadCSV': uploadCSV})
