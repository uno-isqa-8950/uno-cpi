from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})
