from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import Document
from .forms import *


def home(request):
    return render(request, 'home/base_home.html',
                  {'home': home})


def importui(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('importcomplete')
    else:
        form = DocumentForm()
    return render(request, 'import/import.html', {
        'form': form
    })


def importcomplete(request):
    return render(request, 'import/importcomplete.html',
                  {'importcomplete': importcomplete})
