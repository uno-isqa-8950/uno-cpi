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

# Create your views here.



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