from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv, io
from collections import OrderedDict


from .models import *
from .forms import *


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})


# def importui(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         type(form)
#         if form.is_valid():
#             form.save()
#             return redirect('importcomplete')
#     else:
#         form = DocumentForm()
#     return render(request, 'import/import.html', {
#         'form': form})
#
#
# def importcomplete(request):
#     return render(request, 'import/importcomplete.html',
#                   {'importcomplete': importcomplete})


def upload_csv(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/upload_csv.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    # print(type(reader))
    # file_data = csv_file.read().decode('utf-8')
    # lines = file_data.split("\n")
    # print(type(reader))
    for row in reader:
        data_dict = dict(OrderedDict(row))
        # print(data_dict)
        # data_dict = []
        # data_dict["name"] = str(row['name'])
        # data_dict["age"] = int(row['age'])
        # data_dict["length"] = float(row['length'])
        form = PersonForm(data_dict)
        if form.is_valid():
            print(type(form))
            form.save()
    return render(request, 'import/upload_csv.html',
                  {'upload_csv': upload_csv})


def upload_project(request):
    data = {}
    if request.method == "GET":
        return render(request, "import/upload_project.html", data)
    csv_file = request.FILES["csv_file"]
    decoded = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)
    # print(type(reader))
    # file_data = csv_file.read().decode('utf-8')
    # lines = file_data.split("\n")
    # print(type(reader))
    for row in reader:
        data_dict = dict(OrderedDict(row))
        # print(data_dict)
        # data_dict = []
        # data_dict["name"] = str(row['name'])
        # data_dict["age"] = int(row['age'])
        # data_dict["length"] = float(row['length'])
        form = ProjectForm(data_dict)
        if form.is_valid():
            form.save()
    return render(request, 'import/upload_project.html',
                  {'upload_project': upload_project})
